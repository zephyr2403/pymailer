from libs import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from handler import notify,threading,ftext,fclr,change_text
import time 

'''
CLASS FOR HANDLING THE CONNECTION
'''
class CONNECTION(object):
    smtpname=""
    user=""
    pswd=""
    ser=""
    conn=''
    status=0
    def cont_server(self,root,shw,user,pswd,ser):
        if(ser==1):
            CONNECTION.smtpname="smtp.gmail.com"
        elif(ser==2):
            CONNECTION.smtpname="smtp.mail.yahoo.com"
        else:
            CONNECTION.smtpname="smtp-mail.outlook.com"
        try:
            notify(root,shw,"Connecting..",'green')
            CONNECTION.conn=smtplib.SMTP(str(CONNECTION.smtpname),587)
            notify(root,shw,"Connecting...",'green')
            CONNECTION.conn.ehlo()
            notify(root,shw,"Starting Encryption..",'green')
            CONNECTION.conn.starttls()
            notify(root,shw,"Logging in.",'green')
            try:
                CONNECTION.user=user
                CONNECTION.pswd=pswd
                CONNECTION.conn.login(str(CONNECTION.user),str(CONNECTION.pswd))
                CONNECTION.status= 1
            except:
                change_text(root,shw,"Check Details And Enable Less Secure Login On Your Account","Enter Username and Password'","#e63900",fclr,2)
        except:
                change_text(root,shw,"Connection Error.Please Try Again",ftext,"#e63900",fclr,2)
    '''
    MAILS FOUR DIGIT CODE TO THE USER
    '''
    def transfercode(self,code4):
        CONNECTION.conn.sendmail(str(CONNECTION.user),str(CONNECTION.user),'Subject:Four Digit Code\n\nDear User,\n\nYour Speed Code is :'+str(code4)+'\nYou can use this code to Log in the application next time.\n\nC-mailer Bot')

'''
FUNCTION THAT BUILDS THE MAILS
'''
def mailsend(master,lab,user,reciv,sub,mes,*args):
        mess = MIMEMultipart()
        mess['From'] = user
        mess['To'] = reciv
        mess['Subject']=sub
        mess.attach(MIMEText(mes,'plain'))

        if(type(args[0]) is not tuple):
            filename=args[0]
            attach=open(filename,'rb')
            part=MIMEBase('application','octet-stream')
            part.set_payload((attach).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',"attachment; filename= "+filename)
            mess.attach(part)
        mess=mess.as_string()
        t3 = threading.Thread(target=sender,args=(master,lab,str(user),str(reciv),str(mess)))
        t3.start()
'''
FUNCTION THAT SENDS THE MAILS
'''
def sender(master,lab,user,reciv,mess):
    try:
        notify(master,lab,"Sending ...","Green")
        CONNECTION.conn.sendmail(user,reciv,mess)
        change_text(master,lab,"Message Sent to "+str(reciv),"Enter Your Message","green","#454545",2)
    except:
        change_text(master,lab,"Error Occured !! Message Not Sent","Enter Your Message","#e63900","#454545",2)

