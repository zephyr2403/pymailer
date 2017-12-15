import time

ftext="Enter Username And Password"
fclr="#454545"

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

def change_text(root,shw,text,ftext,iclr,fclr,spd):
    shw.config(text=text,fg=iclr);
    root.update()
    time.sleep(spd)
    shw.config(text=ftext,fg=fclr);
    root.update()


def validator(root,shw,user,pswd,var):
        ser=var.get()
        if ser==0:
            change_text(root,shw,"Select Server",ftext,"#e63900","#454545",1)
            return 0
        elif not user:
            change_text(root,shw,"Enter Username",ftext,"#e63900","#454545",1)
            return 0
        elif not pswd:
            change_text(root,shw,"Enter Password",ftext,"#e63900","#454545",1)
            return 0
        elif user.find("@gmail.com")==-1 and user.find("@yahoo.com")==-1 and user.find("@hotmail.com")==-1:
            change_text(root,shw,"Enter Valid Email Addresss",ftext,"#e63900",fclr,1)
            return 0
        elif ser == 1 and user.find("@gmail.com") == -1 or ser==2 and user.find("@yahoo.com") == -1 or ser ==3 and user.find("@outlook.com") == -1 :
            change_text(root,shw,"Incorrect Server Selected",ftext,"#e63900",fclr,1)
            return 0
        else:
            return 1

def codevalidator(root,shw,code4):
        try:
            code4=int(code4)
        except:
            change_text(root,shw,"Enter Valid Number",ftext,"#e63900",fclr,2)
            return 0
        if code4 < 1000 or code4/10000 >0 :
            change_text(root,shw,"Enter 4 Digit Code",ftext,"#e63900",fclr,2)
            return 0
        else:
            return 1
