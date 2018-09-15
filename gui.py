# -*- coding: utf-8 -*-
from libs.GUI.Tkinter import Tk , Label,Button,Text,Radiobutton,Entry,Frame,LEFT,FLAT,GROOVE,IntVar
from libs.GUI import tkFileDialog,tkMessageBox
from speed_DB import SPEEDCODE
import handler
import mailer
attfile=()
log_type=0  # 0  -> Normal Login 1 - >Speed Code


'''
MANAGES INSERTION AND RETRIVAL OF DETAILS FOR DATABASE 
'''
def code_handling(retrieve,*args):
    if(retrieve==0):
        username = args[0]
        password = args[1]
        server = args[2]
        code = SPEEDCODE().insert_detail(username,password,server)
        if code != None:
            t5 = handler.threading.Thread(mailer.CONNECTION().transfercode(code))
            t5.start()
            tkMessageBox.showinfo("Speed Code",'Your Speed Code Is: '+str(code))

    elif(retrieve==1):
        code = args[0]
        username, password , server = SPEEDCODE().retrieve_details(code)
        return username, password , server


'''
CALLS METHOD OF CONNECTION CLASS FOR ESTABLISHING CONNECTION
'''
def connector(root,shw,user,pswd,ser):
    t4 = handler.threading.Thread(target=mailer.CONNECTION().cont_server,args=(root,shw,user,pswd,ser))
    t4.start()
    t4.join()
    if(mailer.CONNECTION.status==1):
        if log_type==0:
            code_handling(0,user,pswd,ser)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        message_box(root,user)


def connectioncheck(root,shw,user,pswd,ser):
    t3 = handler.threading.Thread(target=connector,args=(root,shw,user,pswd,ser))
    t3.start()


'''
CALLS VALIDATOR AND MANAGES ALERT MESSAGE
'''
def validation(root,shw,user,pswd,var):
    if(handler.validator(root,shw,user,pswd,var)==1):
        connectioncheck(root,shw,user,pswd,var.get())


'''
CALLS CODEVALIDATOR AND MANAGES ALERT MESSAGE
'''
def codevalidation(root,shw,code4):
    if(handler.codevalidator(root,shw,code4)==1):
        userName,passWord,server=code_handling(1,code4)
        if(userName == None):
            handler.change_text(root,shw,"Code Not Found",handler.ftext,"#e63900",handler.fclr,2)

        else:
            server=int(server)
            connectioncheck(root,shw,userName,passWord,server)


'''
FUNCTION ALLOWS TO ADD ATTACHMENT
'''
def set_attachment(attbtn):
    global attfile
    if type(attfile) == tuple:
	try:
        	attfile = tkFileDialog.askopenfilename(title="Select File")
	except:
		pass
		
        if type(attfile) == str:
            attbtn.config(text='Remove Attachment')

    else:
        attbtn.config(text='Add Attachment')
        attfile=()


'''
PROVIDE GUI FOR SENDING MAILS
'''
def message_box(master,user):
    for widget in master.winfo_children():
        widget.destroy()

    master.wm_title("Send Message")
    master.configure(background="#DFD8DC")

    lab=Label(master,text="Enter Your Message",font="Tahoma 12 bold",bg="#DFD8DC",fg="#454545")
    lab.grid(row=0,column=0,columnspan=4,padx=(10,0),pady=(15,10))

    to=Label(master,text="To:",font="Tahoma 12 bold",bg="#DFD8DC",fg="#454545")
    to.grid(row=1,column=0,padx=(10,0),pady=(5,20))

    to_ent=Entry(master,width=66,font="Tahoma 12",bg="#DFD8DC",fg="#454545",insertbackground="#454545")
    to_ent.grid(row=1,column=1,columnspan=3,padx=(0,40),pady=(5,20))

    sub=Label(master,text="Subject:",font="Tahoma 12 bold",bg="#DFD8DC",fg="#454545")
    sub.grid(row=2,column=0,padx=(10,0),pady=(5,20))

    sub_ent=Text(master,width=66,height=2,font="Tahoma 12",bg="#DFD8DC",fg="#454545",insertbackground="#454545")
    sub_ent.grid(row=2,column=1,columnspan=3,padx=(0,40),pady=(5,20))

    mess_ent=Text(master,width=66,height=11,font='Tahoma 12',bg="#DFD8DC",fg="#454545",insertbackground="#454545")
    mess_ent.grid(row=3,column=1,columnspan=3,padx=(0,40),pady=(5,20))

    bsend=Button(master,text="Send Mail",relief="groove",command=lambda: mailer.mailsend(master,lab,user,to_ent.get(),sub_ent.get("1.0","end-1c"),mess_ent.get("1.0","end-1c"),attfile),font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
    bsend.grid(row=4,column=1,pady=(0,20))

    attbtn=Button(master,text="Add Attachment",relief="groove",font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
    attbtn.config(command=lambda : set_attachment(attbtn))
    attbtn.grid(row=4,column=2,pady=(0,20))

    lgout=Button(master,text="Logout",relief="groove",command=lambda: flogin(master),font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
    lgout.grid(row=4,column=3,pady=(0,20))


'''
FUNCTION TO CHANGE GUI B/W CODE AND NORMAL LOGIN 
'''
def login_changer(root):
    global log_type
    if log_type ==0:
        root.destroy()
        handler.ftext="Enter Speed Code"
        log_type=1
        codelogin()

    elif log_type==1:
        root.destroy()
        handler.ftext="Enter Username And Password"
        log_type=0
        flogin()


'''
PROVIDES GUI FOR NORMAL LOGIN METHOD
'''
def flogin(*args):
    try:
        args[0].destroy()
    except:
        pass
    root=Tk()
    #For Changing Title Bar
    root.wm_title("SIGN IN")
    root.configure(background="#DFD8DC")
    var=IntVar()

    topframe=Frame(root)
    topframe.pack(side="top")
    topframe.configure(background="#DFD8DC")
    bottomframe=Frame(root)
    bottomframe.pack(side="bottom")
    sev_slet=Label(topframe,text="Select Server: ",font="Tahoma 12 bold",bg="#DFD8DC",fg="#454545")
    sev_slet.pack(side=LEFT)

    grad=Radiobutton(topframe,text="Google",variable=var,value=1,relief="flat",font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC",width=10)
    grad.pack(side=LEFT,padx=10,pady=3)

    yrad=Radiobutton(topframe,text="Yahoo",variable=var,value=2,font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC",width=10)
    yrad.pack(side=LEFT,padx=10,pady=3)


    orad=Radiobutton(topframe,text="Hotmail",variable=var,value=3,relief=FLAT,font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC",width=10)
    orad.pack(side=LEFT,padx=10,pady=3)


    #Creating Label For Username and Password
    bottomframe.configure(background="#DFD8DC")
    username=Label(bottomframe,text="Username",font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
    username.grid(row=2)
    password=Label(bottomframe,text="Password",font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
    password.grid(row=3)

    #Creating Entry Box For Username and Password
    Entry_username=Entry(bottomframe,width=35,fg="#454545",bg="#DFD8DC",font="Tahoma 12",insertbackground="#454545")
    Entry_username.grid(row=2,column=1,pady=5,padx=(10,100))

    Entry_password=Entry(bottomframe,show='*',width=35,fg="#454545",bg="#DFD8DC",font="Tahoma 12 ",insertbackground="#454545")
    Entry_password.grid(row=3,column=1,pady=5,padx=(10,100))

    shw=Label(bottomframe,text="Enter Username and Password",font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
    shw.grid(row=1,columnspan=2)


    #Creating Log in Button
    login_But=Button(bottomframe,text="Log In",relief=GROOVE,width=10,command=lambda:validation(root,shw,Entry_username.get(),Entry_password.get(),var),font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
    login_But.grid(row=4,columnspan=2)

    login_dig=Button(bottomframe,text="LogIn Via Four Digit Code",relief=GROOVE,width=30,command=lambda: login_changer(root),font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
    login_dig.grid(row=5,columnspan=3,pady=5)

    root.mainloop()


'''
PROVIDES GUI FOR LOGIN VIA FOUR DIGIT CODE
'''
def codelogin():
        root=Tk()
        #For Changing Title Bar
        root.wm_title("SIGN IN")
        root.configure(background="#DFD8DC")
        #root.geometry("200x160")

        shw=Label(root,text="Enter Four Digit Code",font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
        shw.grid(row=0,column=2,pady=(10,2))

        Entry_code=Entry(root,width=10,fg="#454545",bg="#DFD8DC",font="Tahoma 12 ",insertbackground="#454545")
        Entry_code.grid(row=1,column=2,pady=(3,2))

        login_But=Button(root,text="Log In",relief=GROOVE,width=8,command=lambda: codevalidation(root,shw,Entry_code.get()),font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
        login_But.grid(row=3,column=2,pady=(3,2))

        login_dig=Button(root,text="Switch To Normal Login",relief=GROOVE,width=25,command=lambda: login_changer(root),font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
        login_dig.grid(row=4,column=2,pady=(3,10),padx=200)

        root.mainloop()


if __name__ == '__main__':
    t1 = handler.threading.Thread(target = flogin)
    t1.start()
