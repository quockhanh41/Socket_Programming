from function_common import *
import socket 
import uuid 
import time 
import mimetypes
import os 
import base64

def check_not(msg, value) :
    if (msg[:3] != value) : print(f"{msg[:3]} reply not received from server")

def answer_server(s, value): 
    msg = s.recv(1024).decode()
    print(msg)
    check_not(msg,value)

def connect_mailserver(s, HOST, PORT) : 
    s.connect((HOST,PORT))
    answer_server(s, "220")

def send_EHLO(s, HOST) :
    s.send(f"EHLO {HOST}\r\n".encode())
    answer_server(s, "250")

def send_mailfrom(s) : 
    FR = readinfo_json("username")
    FR = FR[FR.find('<') : FR.find('>')]
    s.send(f"MAIL FROM: {FR}>\r\n".encode())
    answer_server(s, "250")

def send_RCPTto(s, list_mail) : 
    for i in list_mail["to"]: 
        s.send(f"RCPT TO: <{i}>\r\n".encode())
        answer_server(s, "250")
    for i in list_mail["cc"]: 
        s.send(f"RCPT TO: <{i}>\r\n".encode())
        answer_server(s, "250")
    for i in list_mail["bcc"]: 
        s.send(f"RCPT TO: <{i}>\r\n".encode())
        answer_server(s, "250")

def send_DATA(s) : 
    s.send("DATA\r\n".encode())
    answer_server(s, "354")

def get_content_type(file_path) : 
    mime_type, encoding = mimetypes.guess_type(file_path)
    return mime_type 

def send_file(s, file_path) :
    encoded_text = ""
    with open(file_path,"rb") as f:
        binary_data = f.read()
        encoded_data = base64.b64encode(binary_data)
        encoded_text = encoded_data.decode()
        for i in range(0,len(encoded_text),1024): 
            msg = encoded_text[i : i + 1024]
            s.send(msg.encode())
            s.send("\r\n".encode())


def send_content(s, list_mail, list_file, subject_mail, content_mail) : 
    boundary = readinfo_json("boundary")
    s.send(f"multipart/mixed; boundary={boundary}\r\n".encode())

    # thong tin message id 
    msg = readinfo_json("username")
    Message_ID = str(uuid.uuid4()) + msg[msg.find("@") : ]
    s.send(f"Message-ID: <{Message_ID}>\r\n".encode())

    # thong in data
    localtime = time.asctime(time.localtime(time.time()))
    s.send(f"Date: {localtime}\r\n".encode())
    
    # thong tin mime-version
    msg = readinfo_json("mime-version")
    s.send(f"MIME-Version: {msg}\r\n".encode())

    # thong tin user-Agent 
    msg = readinfo_json("user-agent")
    s.send(f"User-Agent: {msg}\r\n".encode())

    # thng tin Content-Language 
    msg = readinfo_json("content-language")
    s.send(f"Content-Language: {msg}\r\n".encode())

    # thong tin mail to
    for i in "to","cc": 
        if len(list_mail[i]) == 0: continue
        s.send((i + ": ").encode())
        for j in range(0,len(list_mail[i]) - 1): s.send((list_mail[i][j] + ",").encode())
        s.send((list_mail[i][len(list_mail[i]) - 1] + '\r\n').encode())

    # thong tin from 
    msg = readinfo_json("username")
    s.send(f"From: {msg}\r\n".encode())

    # thong tin subject va content 
    s.send(f"Subject: {subject_mail}\r\n".encode())

    # gui file 
    s.send(f"this is a multi-part message in MIME format\r\n{boundary}\r\n".encode())
    s.send("Content-Type: text/plain; charset=UTF-8; format=flowed\r\nContent-Transfer-Encoding: 7bit\r\n".encode())
    
    # thong tin content 
    s.send(f"{content_mail}\r\n".encode())

    for file_path in list_file: 
        s.send((boundary + "\r\n").encode())
        content_type = get_content_type(file_path)
        name = os.path.basename(file_path)
        s.send(f"Content-Type: {content_type}; name={name}\r\n".encode())
        s.send(f"Content-Disposition: attachment; filename={name}\r\n".encode())
        s.send(f"Content-Transfer-Encodeing: base64\r\n".encode()) 
        send_file(s, file_path)
    s.send((boundary + "\r\n").encode())
    s.send(".\r\n".encode())
    msg = s.recv(1024).decode()
    if "accepted" in msg: 
        print("Da gui mail thanh cong")
    s.send("QUIT\r\n".encode())


def client_mail(list_mail, list_file, subject_mail, content_mail) : 
    HOST = readinfo_json("mailserver")
    PORT = readinfo_json("SMTP")
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        connect_mailserver(s, HOST, PORT)
        send_EHLO(s, HOST)
        send_mailfrom(s)
        send_RCPTto(s, list_mail)
        send_DATA(s)
        send_content(s, list_mail, list_file, subject_mail, content_mail)
