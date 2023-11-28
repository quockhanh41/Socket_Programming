from msilib import Binary
from typing import BinaryIO
from urllib.request import FancyURLopener
from function_common import *
import socket 
import json 
import base64 

def send_LOGIN(s) : 
    s.send(("USER " + "to1@gmail.com" + "\r\n").encode())
    msg = s.recv(1024)
    s.send(("PASS " + readinfo_json("password") + "\r\n").encode())
    msg = s.recv(1024)

def send_STAT(s) : 
    s.send(("STAT\r\n").encode())
    msg = s.recv(1024).decode().split()
    return msg[1]
    
def send_LIST(s) : 
    s.send(("LIST\r\n").encode())
    msg = s.recv(1024)

def send_UIDL(s) :
    s.send("UIDL\r\n".encode())
    msg = s.recv(1024).decode().split()
    L = []
    for i in range(2,len(msg),2) : 
        L.append(msg[i])
    return L

def download_mail(s, number_mail):
    s.send(f"RETR {number_mail}\r\n".encode())
    con = s.recv(1024).decode()
    file_size = int(con.split()[1]) 
    file_size -= 1024
    while file_size >= 0: 
        data = s.recv(1024)
        con += data.decode()
        file_size -= 1024
    return con 

def readinfo_mail(s, number_mail) :
    con = download_mail(s, number_mail)
    boundary = readinfo_json("boundary")

    From = con[con.find("From:") + 6: con.find("Subject") - 2]

    con = con.split(f"{boundary}\r\n")
    tmp = str(con[1])
    subject_mail = tmp[tmp.find("Subject:") + 9: tmp.find(boundary) - 46]
    con[2] = con[2].split("\r\n")

    content_mail = con[2][2]
    
    list_file = []
    for i in range(3,len(con) - 1):
        New = con[i].split("\r\n")
        cont = ""
        file_name = New[0][New[0].find('name=') + 5: ]
        for i in range(3,len(New)) : cont += New[i]
        #out_path = "d:\\send\\" + file_name 
        list_file.append((file_name,cont))
        #decode_base64_to_pdf(cont, out_path)
    return From, subject_mail, content_mail, list_file
      

def received_mailserver() : 
    HOST = readinfo_json("mailserver")
    PORT = readinfo_json("POP3")
    read_mail = {}
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s: 
        s.connect((HOST,PORT))
        msg = s.recv(1024)
        s.send("CAPA\r\n".encode())
        msg = s.recv(1024)
        send_LOGIN(s)
        number_of_mail = int(send_STAT(s))
        send_LIST(s)
        list_namemail = send_UIDL(s)
        mail = []
        for i in range(1,number_of_mail + 1): 
            From, subject, content, list_file = readinfo_mail(s, i)
            mail.append([list_namemail[i - 1], From, subject, content, list_file])
        return mail 