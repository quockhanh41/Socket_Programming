import os
import base64
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_user_folder(email):
    folders=["Inbox","Project","Important","Work","Spam"]
    path="D:\Gmail\\"+email
    create_folder(path)
    for folder in folders:
        create_folder(path+f"\\{folder}")
        create_folder(path+f"\\{folder}"+"\\Unread")
        create_folder(path+f"\\{folder}"+"\\Read")

def getFileList(folder_path):
    files = os.listdir(folder_path)
    file_names = [os.path.basename(file) for file in files]
    return file_names

def printMsgList(file_list,sender_email,choice,status):
    folder=["Inbox","Project","Important","Work","Spam"]
    sender_list=[]
    subject_list=[]
    for file in file_list:
        sender_list.append(getSender(f'D:\\Gmail\\{sender_email}\\{folder[choice-1]}\\{status}\\{file}'))
        subject_list.append(getSubject(f'D:\\Gmail\\{sender_email}\\{folder[choice-1]}\\{status}\\{file}'))
    for i in range(0,len(sender_list)):
        if(status=='Unread'):
            print('(chưa đọc)<'+sender_list[i]+'>,<'+subject_list[i]+'>')
        elif(status=='Read'): 
            print('<'+sender_list[i]+'>,<'+subject_list[i]+'>')

def getSender(msg_path):
    with open(msg_path,'r') as file:
        email_content=file.read()
    sender=email_content[email_content.find('From: ')+6:email_content.find('To: ')-2]
    return sender

def getRecipient(msg_path):
    with open(msg_path,'r',newline='\n') as file:
        email_content=file.read()
    recipient_list=email_content[email_content.find('To: '):email_content.find('MIME-Version: ')-2]
    return recipient_list

def getSubject(msg_path):
    with open(msg_path,'r') as file:
        email_content=file.read()
    subject=email_content[email_content.find('Subject: ')+9:email_content.find('From: ')-2]
    return subject

def getBody(msg_path):
    with open(msg_path,'r',newline='\n') as file:
        email_content=file.read()
    email_content_list=email_content.split('--my_boundary')
    body=email_content_list[1][email_content_list[1].find('charset="utf-8"')+18:email_content_list[1].rfind('\r\n')-4]
    return body

def getFile(msg_path):
    with open(msg_path,'r',newline='\n') as file:
        email_content=file.read()
    email_content_list=email_content.split('--my_boundary')
    file_list=[]
    for i in range(2,len(email_content_list)-1):
        filename=email_content_list[i][email_content_list[i].find('filename="')+10:email_content_list[i].rfind('"')]
        file_data=email_content_list[i][email_content_list[i].rfind('"')+7:email_content_list[i].rfind('--my_boundary')-2]
        file_list.append([filename,file_data])
    return file_list

def getEmail(msg_path):
    email= f'Subject: {getSubject(msg_path)}\r\nFrom: {getSender(msg_path)}\r\n{getRecipient(msg_path)}\r\nContent: {getBody(msg_path)}\r\n'
    file_list=getFile(msg_path)
    for file in file_list:
        filename,file_data=file
        email+=f'File: {filename}\r\n'
    return email,file_list

def downloadFile(file,path):
    filename,file_data=file
    path+=f'\\{filename}'
    with open(path, 'wb') as attachment_file:
        attachment_file.write(base64.b64decode(file_data))