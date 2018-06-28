import os, sys
from libs import sqlite3
from handler import encrypt, decrypt
import random 

'''
CHANGING DIRECTORY TO DIRECTORY WHERE THE FILES ARE LOCATED
'''
if(os.path.dirname(sys.argv[0])==''):
    pass
else:
    os.chdir(os.path.dirname(sys.argv[0]))

class SPEEDCODE(object):
    
    def __init__(self):
        '''
        SELECTING DATA BASE AND CREATING TABLE IF PREVIOUSLY NOT CREATED
        '''
        self.sql_conn = sqlite3.connect('speedcode.db')
        self.cursor = self.sql_conn.cursor()
        try:
            self.cursor.execute('CREATE TABLE codes (username varchar(300) not null,password varchar(300) not null,servercode int not null,code VARCHAR(20) primary key)')
            self.sql_conn.commit()
        except:
            pass 
    '''
    FUNCTION TO INSERT NEWUSER IN THE DATABASE AND PROVIDING THEM SPEED CODE
    '''
    def insert_detail(self,username,passwd,ser):

        self.cursor.execute('SELECT username,password FROM codes')
        detvar = self.cursor.fetchall()
        check = 1
        for i in range(len(detvar)):
            if(username == decrypt(str(detvar[0][0])) and passwd == decrypt(str(detvar[0][1]))):
                check = 0
                break

        if check == 1:
            username = encrypt(username)
            passwd = encrypt(passwd)
            code = random.randint(1000,9999)
            code_c = code
            self.cursor.execute('select code from codes')
            code_tuples = self.cursor.fetchall()
            code_list= []
 
            for i in range(len(code_tuples)):
                code_list.append(decrypt(str(code_tuples[i][0])))

            #If generated code already exists in the database changing it
            while str(code) in code_list:
                code = random.randint(1000,9999)
                code_c = code
            
            code = encrypt(str(code))
            self.cursor.execute("INSERT INTO codes (username,password,servercode,code) VALUES('%s','%s','%i','%s')"%(username,passwd,ser,code))
            self.sql_conn.commit()
            return code_c
        else:
            return None
    '''
    FUNCTION TO RETRIVE USERNAME AND PASSWORD FROM SPEED CODE
    '''
    def retrieve_details(self,code):
        code = str(code)
        self.cursor.execute("select * from codes")
        detvar = self.cursor.fetchall()

        for i in range(len(detvar)):
            if str(code) == decrypt(str(detvar[i][3])):
                return decrypt(str(detvar[i][0])), decrypt(str(detvar[i][1])),detvar[i][2]
        
        return None, None, None



