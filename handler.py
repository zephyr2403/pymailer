import time
import threading
from string import letters
from random import choice

ftext="Enter Username And Password"
fclr="#454545"

'''
ENCRYPT THE USERNAME, PASSWORD AND CODE BEFORE INSERTING IN DATABASE
'''
def encrypt(string):
    random_ = letters + '0123456789' 
    string = bytearray(string)
    for i in range(len(string)):
        if string[i] > 96 and string[i] < 123:
            if string[i] > 118:
                val = string[i] - 118   + 64
                string[i] = val
            else:
                string[i] = string[i] - 28
        elif string[i] > 64 and string[i] < 91:
            if string[i] > 86:
                val = string[i] - 86   + 96
                string[i] = val
            else:
                string[i] = string[i] + 36
        elif string[i] > 47 and string[i] < 58:
            if string[i] > 53:
                val = string[i] - 53 + 47
                string[i] = val 
            else:
                string[i] = string[i] + 4

    string = str(string) 
    string = list(string)
    string = [choice(random_) + letter + choice(random_) for letter in string]
    string = ''.join(string)
    return str(string)

'''
DECRYPT USERNAME, PASSWORD AND CODE WHICH ARE IN DATABASE
'''
def decrypt(string):
    string = [string[i:i+3] for i in range(0,len(string),3)]
    string = [item[1] for item in string]
    string = ''.join(string)
    string = bytearray(string)

    for i in range(len(string)):
        if string[i] > 64 and string[i] < 91 :
            if string[i] <  69 :
                string[i] = string[i] - 64   + 118
            else:
                string[i] = string[i] + 28

        elif string[i] > 96 and string[i] < 123:
            if string[i] < 101:
                string[i] = string[i] - 96 + 86
            else:
                string[i] = string[i] - 36
        elif string[i] > 47 and string[i] < 58:
            if string[i] < 52:
                string[i] = string[i] - 47 + 53
            else :
                string[i] = string[i] - 4
    
    return str(string)

'''
FUNCTION THAT NOTIFY USERS OF CURRENT STATUS 
'''
def notify(root,shw,text,clr):
    shw.config(text=text,fg=clr)
    root.update()
'''
ALERT USERS WHEN SOMETHING UNDESIRED HAPPENS
'''
def alert_message(root,shw,text,ftext,iclr,fclr,spd):
    shw.config(text=text,fg=iclr)
    root.update()
    time.sleep(spd)
    shw.config(text=ftext,fg=fclr)
    root.update()

def change_text(root,shw,text,ftext,iclr,fclr,spd):
    t1 = threading.Thread(target=alert_message,args=(root,shw,text,ftext,iclr,fclr,spd))
    t1.start()

'''
FUNCTION TO VALIDATE WHETHER THE DETAILS ENTERED IN THE LOGIN FORM ARE VALID OR NOT
'''
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
'''
FUNCTION TO VALIDATE WHETHER FOUR DIGIT CODE IS VALID OR NOT 
'''
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
