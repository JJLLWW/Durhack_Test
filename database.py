from ast import Pass
from collections import namedtuple
import sqlite3

def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS U
            (NAME TEXT,
            PASSWORD TEXT,
            LANGUAGEID INTEGER,
            EMAIL TEXT);
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS M
            (SENDER TEXT,
            RECEIVER TEXT,
            MESSAGE TEXT,
            NUMBER INTEGER PRIMARY KEY AUTOINCREMENT);
    """)


class user:
    def __init__(self, name, password, langid, email):
        self.name = name
        self.Pass = password
        self.langid = langid
        self.email = email
        self.all = [self.name, self.Pass, self.langid, self.email]

def add_user(Name, Pass, Langid, Email, cursor):
    exist_name = ""
    cursor.execute("""
        SELECT NAME FROM U where NAME = ?
    """, [Name])
    # if there is an entry already we don't do anything
    for row in cursor:
        # if the name exists, check the password
        exist_name = (row)
    if exist_name == "":
        cursor.execute("""
        INSERT INTO U (NAME, PASSWORD, LANGUAGEID, EMAIL) VALUES(?, ?, ?, ?)
        """, [Name, Pass, Langid, Email])  
    else:
        print("user already exists")

#add_user(234, "Olivia", "olivia", "45456", "@olivia.com")   

def add_message(user1, user2, text, cursor):
    cursor.execute("""
    INSERT INTO M (SENDER, RECEIVER, MESSAGE) VALUES(?, ?, ?)
    """, [user1, user2, text])

def get_user(name, cursor):
    cursor.execute("""
        SELECT * FROM U where NAME = ?
    """, [name])
    result = ""
    for row in cursor:
        newusr = user(row[0], row[1], row[2], row[3])
        return newusr

def get_message(user1, user2, cursor):
    cursor.execute(""" 
    SELECT NUMBER FROM M where (SENDER,RECEIVER) = (?, ?) 
    """, [user1, user2])
    result = []
    for row in cursor:
        result.append(row)

    cursor.execute(""" 
    SELECT NUMBER FROM M where (RECEIVER, SENDER) = (?, ?) 
    """, [user1, user2])
    for row in cursor:
        result.append(row)
    res=[]
    for i in result:
        res.append(i[0])

    res.sort()
    print(res,"result")
    conversation = []

    for num in res:
        cursor.execute(""" 
        SELECT SENDER, RECEIVER, MESSAGE FROM M where (NUMBER) = (?) 
        """, [num])
        for row in cursor:
           conversation.append(row)

    print(conversation)



SUCCESS, ERR_NOUSR, ERR_WRONGPASS = 0, 1, 2
def errmsg_from_code(code):
    if code == SUCCESS:
        print("success")
    elif code == ERR_NOUSR:
        print("no user")
    elif code == ERR_WRONGPASS:
        print("wrong password")

def verify_user(name, password, cursor):
    real_password = None
    cursor.execute("""
        SELECT NAME FROM U where NAME = ?
    """, [name])
    print(name)
    for row in cursor:
        # if the name exists, check the password
        cursor.execute("""
        SELECT PASSWORD FROM U where NAME = ?
        """, [name])
        for row in cursor:
            real_password = row[0]
            print(f"password was {real_password}")
        if password == real_password:
            return SUCCESS
        else:
            return ERR_WRONGPASS
    return ERR_NOUSR



