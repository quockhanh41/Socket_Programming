import socket
import base64
import os
def getAttachmentName(s): 
    return s[s.find('"')+1:len(s)-1]
   
def danh_sach_thu_muc(duong_dan):
    danh_sach_thu_muc = []
    for ten in os.listdir(duong_dan):
        duong_dan_day_du = os.path.join(duong_dan, ten)
        if os.path.isdir(duong_dan_day_du):
            danh_sach_thu_muc.append(ten)
    return danh_sach_thu_muc
    
def path_message(path_folder):
    amount_message_cur = len(danh_sach_thu_muc(path_folder))
    newFolder = 'Message ' + str(amount_message_cur +1 ) 
    path_newFolder = os.path.join(path_folder,newFolder) 
    if not os.path.exists(path_newFolder):
        os.makedirs(path_newFolder)
    return path_newFolder
    
    
def folder_filtering(content,project_keywords,important_keywords,work_keywords,spam_keywords):
    list_folder=[]
    From = content[content.find('From: ') + 6:content.find('To: ') - 2]
    Subject = content[content.find('Subject: ') + 9:content.find('From: ') - 2]
    Body = content[content.find('Content: ') + 9:]
    for project_keyword in project_keywords:
        if From == project_keyword:
            list_folder.append(r"D:\MailBox\Project\Unread")
            break
    for important_keyword in important_keywords:
        if Subject.find(important_keyword) != -1:
            list_folder.append(r"D:\MailBox\Important\Unread")
            break
    for work_keyword in work_keywords:
        if Body.find(work_keyword) != -1:
            list_folder.append(r"D:\MailBox\Work\Unread")
            break
    for spam_keyword in spam_keywords:
        if Body.find(spam_keyword)!= -1 or Subject.find(spam_keyword) != -1:
            list_folder.append(r"D:\MailBox\Spam\Unread")
            break
    if not list_folder:
        list_folder.append(r"D:\MailBox\Inbox\Unread")
    return list_folder


def retrieve_email_with_attachment_socket( username, password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pop_conn:
        pop_conn.connect(('localhost', 3335))

        response = pop_conn.recv(1024).decode()
        print(response)

        # Send user credentials
        pop_conn.sendall(f'USER {username}\r\n'.encode())
        response = pop_conn.recv(1024).decode()
        print(response)

        pop_conn.sendall(f'PASS {password}\r\n'.encode())
        response = pop_conn.recv(1024).decode()
        print(response)
        # Get the number of messages in the mailbox
        pop_conn.sendall(b'LIST\r\n')
        response = pop_conn.recv(1024).decode()
        print(response)

        # Get the number of messages in the mailbox
        num_messages = len(response.splitlines())-2
        # Retrieve each email
        for i in range(1, num_messages + 1):
            # Retrieve the email by message number
            pop_conn.sendall(f'RETR {i}\r\n'.encode())
            email=''
            while response := pop_conn.recv(1024).decode():
                email+=response
                if response.find('--my_boundary--')!=-1:
                    break
            lines=email.splitlines()
            email='\r\n'.join(lines[1:])


            email_content_list=email.split('\r\n\r\n')

            ##  xử lí file config  ##

            project_keywords ={'ahihi@testing.com', 'ahuu@testing.com'}
            important_keywords={"urgent", "ASAP"}
            work_keywords={"report", "meeting"}
            spam_keywords={"virus", "hack", "crack"}

            email_content = email_content_list[0] + '\r\nContent: ' + email_content_list[3]

            paths_folder = folder_filtering(email_content,project_keywords,important_keywords,work_keywords,spam_keywords)
            for path in paths_folder:
                print(path)
                pathMessage = path_message(path) # tạo folder message mới 
                newFile = email_content[email_content.find('Subject: ')+9:email_content.find('From: ')-2]
                   
                path_newFile = os.path.join(pathMessage,newFile)
                with open(path_newFile, 'w') as attachment_file:
                    attachment_file.write(email_content)  

                for i in range(4,len(email_content_list)-1 , 2):
                    attachmentName = getAttachmentName(email_content_list[i])
                    path_attachment = os.path.join(pathMessage,attachmentName)
                    with open(path_attachment, 'wb') as attachment_file:
                        attachment_file.write(base64.b64decode(email_content_list[i+1]))   
                        print(f"Attachment saved: {attachmentName}")
                
        # Quit the session
        pop_conn.sendall(b'QUIT\r\n')
        response = pop_conn.recv(1024).decode()
        print(response)

# Set your POP3 server details

pop3_username = 'qknetwork41@gmail.com'
pop3_password = '25092004'  # Consider using app-specific password for security

# Call the retrieve_email_with_attachment_socket function
retrieve_email_with_attachment_socket( pop3_username, pop3_password)

