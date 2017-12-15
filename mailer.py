import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from handler import change_text,ftext,fclr
class CONNECTION(object):
    smtpname=""
    user=""
    pswd=""
    ser=""
    def cont_server(self,root,shw,user,pswd,ser):
        global conn
        if(ser==1):
            CONNECTION.smtpname="smtp.gmail.com"
        elif(ser==2):
            CONNECTION.smtpname="smtp.mail.yahoo.com"
        else:
            CONNECTION.smtpname="smtp-mail.outlook.com"
        try:
            change_text(root,shw,"Connecting.","Connecting..","#00e6e6","#00e6e6",1)
            conn=smtplib.SMTP(str(CONNECTION.smtpname),587)
            change_text(root,shw,"Connecting...","Connected","#00e6e6","#66cc00",1)
            conn.ehlo()
            change_text(root,shw,"Connected","Starting Encrption Before Logging in","#66cc00","#00e6e6",1)
            conn.starttls()
            change_text(root,shw,"Successfully Encrpted","Logging In..","#66cc00","#00e6e6",1)
            try:
                CONNECTION.user=user
                CONNECTION.pswd=pswd
                conn.login(str(CONNECTION.user),str(CONNECTION.pswd))
                #change_text(root,shw,"Logging In....","Successfully Logged In ","#00e6e6","#66cc00",1)
                return 1
            except:
                change_text(root,shw,"Login Failed.","Make Sure Username and Password is Correct","#e63900","#e63900",1)
                change_text(root,shw,"Make Sure Username and Password is Correct","Enable Less Secure Login On Your Account","#e63900",fclr,2)
                change_text(root,shw,"Enable Less Secure Login On Your Account",ftext,"#e63900",fclr,2)
                return 0
        except:
                change_text(root,shw,"No Internet Connection.Please Try Again",ftext,"#e63900",fclr,2)
                return 0

    def reconnect(self):
        conn = smtplib.SMTP(CONNECTION.smtpname,587)
        conn.ehlo()
        conn.starttls()
        conn.login(str(CONNECTION.user),str(CONNECTION.pswd))
        return conn

    def transfercode(self,code4):
        print "--"
        conn.sendmail(str(CONNECTION.user),str(CONNECTION.user),'Subject:Four Digit Code\n\nDear User\n\tYour Speed Code is :'+str(code4))
        print "--++"
def mailsend(master,lab,user,reciv,sub,mes,*args):
        mess = MIMEMultipart()
        mess['From'] = user
        mess['To'] = reciv
        mess['Subject']=sub
        mess.attach(MIMEText(mes,'plain'))

        if(args[0] is not ""):
            filename=args[0]
            attach=open(filename,'rb')
            part=MIMEBase('application','octet-stream')
            part.set_payload((attach).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',"attachment; filename= "+filename)
            mess.attach(part)
        mess=mess.as_string()
        try:
            conn.sendmail(str(user),str(reciv),str(mess))
            change_text(master,lab,"Message Sent to "+str(reciv),"Enter Your Message","green","#454545",2)
        except:
            change_text(master,lab,"Reconnecting..","Reconnecting...","green","green",1)
            conn=CONNECTION().reconnect()
            try:
                conn.sendmail(str(user),str(reciv),str(mess))
                change_text(master,lab,"Message Sent to "+str(reciv),"Enter Your Message","green","#454545",2)
            except:
                change_text(master,lab,"Message Not Sent","Enter Your Message","#e63900","#454545",2)
