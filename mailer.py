# -*- coding: utf-8 -*-
from Tkinter import *
import time
import smtplib
import math
import inspect as iz
import os
import random

#ser = -2
def change_text(root,shw,text,ftext,iclr,fclr,spd):
    shw.config(text=text,fg=iclr);
    root.update()
    time.sleep(spd)
    shw.config(text=ftext,fg=fclr);
    root.update()

def blink(widget,iclr,fclr,spd):
    widget.config(bg=fclr)
    root.update()
    time.sleep(spd)
    widget.config(bg=iclr);
    root.update()

def animate(start,end,xrat,yrat,spd,root):
    for i in range(start,end,4):
        root.geometry(str(i*xrat)+"x"+str(int(math.ceil(i*yrat+i/2))))
        root.update()
        time.sleep(spd)

def cont_server(root,shw,user,pswd,ser):
    global conn
    if(ser==1):
        smtpname="smtp.gmail.com"
    elif(ser==2):
        smtpname="smtp.mail.yahoo.com"
    else:
        smtpname="smtp-mail.outlook.com"
    try:
        change_text(root,shw,"Connecting.","Connecting..","#00cccc","#00cccc",1)
        conn=smtplib.SMTP(str(smtpname),587)
        change_text(root,shw,"Connecting...","Connected","#00cccc","#66cc00",1)
        conn.ehlo()
        change_text(root,shw,"Connected","Starting Encrption Before Logging in","#66cc00","#00cccc",1)
        conn.starttls()
        change_text(root,shw,"Successfully Encrpted","Logging In..","#66cc00","#00cccc",1)
        try:
            conn.login(str(user),str(pswd))
            change_text(root,shw,"Logging In....","Successfully Logged In ","#00cccc","#66cc00",1)
            if log_type==0:
               code4=random.randint(1000,9999)
               print code4
               code_handling(code4,0,user,pswd,ser)
            message_box(root,user)
        except:
            change_text(root,shw,"Login Failed.","Make Sure Username and Password is Correct","red","red",1)
            change_text(root,shw,"Make Sure Username and Password is Correct","Enable Less Secure Login On Your Account","red",fclr,2)
            change_text(root,shw,"Enable Less Secure Login On Your Account",ftext,"red",fclr,2)
    except:
            change_text(root,shw,"No Internet Connection.Please Try Again",ftext,"red",fclr,2)




def encrypt(use):
    use=bytearray(use)
    for i in range(len(use)):
        if(use[i]>96 and use[i]<123):
            use[i]=use[i]-14
        elif(use[i]==46):
            use[i]=62
        elif(use[i]==64):
            use[i]=63
    return str(use)

def decrypt(use):
    use=bytearray(use)
    for i in range(len(use)):
        if(use[i]>82 and use[i]<109):
            use[i]=use[i]+14
        elif(use[i]==62):
            use[i]=46
        elif(use[i]==63):
            use[i]=64
    return str(use)

def code_handling(code4,z,*args):
    print "exe"
    global ser
    p=os.path.dirname(iz.stack()[0][1])
    if not os.path.exists(p+r'/db'):
            fw=open(p+r'/db','w')
            fw.close()
    fw=open(p+r'/db','r')
    re=fw.read()
    fw.close()
    if(z==0):
        print "exe"
        user = args[0]
        pswd = args[1]
        ser = args[2]
        print user,pswd
        if re.find(encrypt(user))==-1 and re.find(encrypt(pswd))==-1:
            print "exe1"
            while(str(code4) in re):
                code4=random.randint(1000,999)
            fw=open(p+r'/db','a')
            fw.write(str(ser)+str(code4)+str(encrypt(user))+'x'+str(encrypt(pswd))+'\n')
            fw.close()
            conn.sendmail(str(user),str(user),'Subject:Four Digit Code\n\nDear User\n\tYour Speed Code is :'+str(code4))
            z=Tk()
            z.wm_title('Speed Code Details')
            m=Label(z,text='Your Speed Code Is: '+str(code4))
            m.pack(padx=100)
    elif(z==1):
            if(re.find(str(code4))!=-1):
                ser=re[re.find(str(code4))-1]
                re=re[re.find(str(code4)):]
                user=decrypt(re[re.find(str(code4))+4:re.find('x')])
                pswd=decrypt(re[re.find('x')+1:re.find('\n')])
                return user ,pswd,ser
            else:
                return 'false','false','false'



def codevalidate(root,shw,code4):
        try:
            code4=int(code4)
        except:
            change_text(root,shw,"Enter Valid Number",ftext,"red",fclr,2)
        if code4 < 1000 or code4/10000 >0 :
            change_text(root,shw,"Enter 4 Digit Code",ftext,"red",fclr,2)
        else:
            user,pswd,ser=code_handling(code4,1)
            if(user == 'false'):
                change_text(root,shw,"Code Not Found",ftext,"red",fclr,2)
            else:
                ser=int(ser)
                cont_server(root,shw,user,pswd,ser)


def validation(root,shw,user,pswd,var):
        ser=var.get()
        if ser==0:
            change_text(root,shw,"Select Server",ftext,"red","#454545",1)
        elif not user:
            change_text(root,shw,"Enter Username",ftext,"red","#454545",1)
        elif not pswd:
            change_text(root,shw,"Enter Password",ftext,"red","#454545",1)
        elif user.find("@gmail.com")==-1 and user.find("@yahoo.com")==-1 and user.find("@hotmail.com")==-1:
            change_text(root,shw,"Enter Valid Email Addresss",ftext,"red",fclr,1)
        elif ser == 1 and user.find("@gmail.com") == -1 or ser==2 and user.find("@yahoo.com") == -1 or ser ==3 and user.find("@outlook.com") == -1 :
            change_text(root,shw,"Incorrect Server Selected",ftext,"red",fclr,1)
        else:
            cont_server(root,shw,user,pswd,ser)


def takedet(user):
        mess = "Subject:" + sub_ent.get("1.0","end-1c") + "\n\n" + mess_ent.get("1.0","end-1c")
        reciv=to_ent.get()
        try:
            conn.sendmail(str(user),str(reciv),str(mess))
        except:
            pass

def message_box(root,user):
    root.destroy()
    master=Tk()
    master.wm_title("Send Message")
    master.configure(background="#DFD8DC")
    #global to_ent,sub_ent,mess_ent
    to=Label(master,text="To:",font="Tahoma 12 bold",bg="#DFD8DC",fg="#454545")
    to.grid(row=0,column=0,padx=(10,0),pady=(5,20))

    to_ent=Entry(master,width=66,font="Tahoma 12",relief="groove",bg="#DFD8DC",fg="#454545",insertbackground="#454545")
    to_ent.grid(row=0,column=1,padx=(0,10),pady=(5,20))

    sub=Label(master,text="Subject:",font="Tahoma 12 bold",bg="#DFD8DC",fg="#454545")
    sub.grid(row=1,column=0,padx=(10,0),pady=(5,20))

    sub_ent=Text(master,width=66,height=2,font="Tahoma 12",relief="groove",bg="#DFD8DC",fg="#454545",insertbackground="#454545")
    sub_ent.grid(row=1,column=1,padx=(0,10),pady=(5,20))

    mess_ent=Text(master,width=66,height=11,font='Tahoma 12',relief="groove",bg="#DFD8DC",fg="#454545",insertbackground="#454545")
    mess_ent.grid(row=2,column=1,padx=(0,10),pady=(5,20))

    mess = "Subject:" + sub_ent.get("1.0","end-1c") + "\n\n" + mess_ent.get("1.0","end-1c")

    bsend=Button(master,text="Send Message",relief="groove",command=lambda: takedet(user),font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
    bsend.grid(row=3,column=1,columnspan=2,pady=(0,10))

    master.mainloop()

def dig_log(root):
    global log_type
    if log_type ==0:
        root.destroy()
        ftext="Enter Speed Code"
        log_type=1
        codelogin()


    elif log_type==1:
        root.destroy()
        ftext="Enter Username And Password"
        log_type=0
        flogin()


mess=""
log_type=0  # 0  -> Normal Login 1 - >Speed Code
ftext="Enter Username And Password"


fclr="#454545"
def flogin(*args):
    try:
        args[0].destroy()
    except:
        pass
    root=Tk()
    #For Changing Title Bar
    root.wm_title("SIGN IN")
    root.configure(background="#DFD8DC")
    root.geometry("676x220")
    #animate(1,160,4,1,.005,root)
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

    code=Label(bottomframe,text="Four Digit Code :",font="Tahoma 12 ",fg="#454545",bg="#DFD8DC")
    #---code.grid(row=3)
    Entry_code=Entry(bottomframe,width=35,fg="#454545",bg="#DFD8DC",font="Tahoma 12 ",insertbackground="#454545")
    #--Entry_code.grid(row=2,column=1,pady=5,padx=(10,100))

    shw=Label(bottomframe,text="Enter Username and Password",font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
    shw.grid(row=1,columnspan=2)


    #Creating Log in Button
    login_But=Button(bottomframe,text="Log In",relief=GROOVE,width=10,command=lambda: validation(root,shw,Entry_username.get(),Entry_password.get(),var),font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
    login_But.grid(row=4,columnspan=2)

    login_dig=Button(bottomframe,text="LogIn Via Four Digit Code",relief=GROOVE,width=30,command=lambda: dig_log(root),font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
    login_dig.grid(row=5,columnspan=3,pady=5)

    root.mainloop()

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

        login_But=Button(root,text="Log In",relief=GROOVE,width=8,command=lambda: codevalidate(root,shw,Entry_code.get()),font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
        login_But.grid(row=3,column=2,pady=(3,2))

        login_dig=Button(root,text="Switch To Normal Login",relief=GROOVE,width=25,command=lambda: dig_log(root),font="Tahoma 12 bold",fg="#454545",bg="#DFD8DC")
        login_dig.grid(row=4,column=2,pady=(3,10),padx=200)

flogin()
