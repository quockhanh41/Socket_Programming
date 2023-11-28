import socket
import base64
import os
from path_handling import path_message
from path_handling import folder_filtering


def getAttachmentName(s): 
    return s[s.find('"')+1:len(s)-1]

def retrieve_email_with_attachment_socket( username, password,pop3_host):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pop_conn:
        pop_conn.connect((pop3_host, 3335))

        response = pop_conn.recv(1024).decode()
        #print(response)

        # Send user credentials
        pop_conn.sendall(f'USER {username}\r\n'.encode())
        response = pop_conn.recv(1024).decode()
        #print(response)

        pop_conn.sendall(f'PASS {password}\r\n'.encode())
        response = pop_conn.recv(1024).decode()
        #print(response)
        # Get the number of messages in the mailbox
        pop_conn.sendall(b'LIST\r\n')
        response = pop_conn.recv(1024).decode()
        #print(response)

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
                #print(path)
                pathMessage = path_message(path) # tạo folder message mới 
                newFile = email_content[email_content.find('Subject: ')+9:email_content.find('From: ')-2]
                   
                path_newFile = os.path.join(pathMessage,newFile)
                #print(path_newFile)
                with open(path_newFile, 'w') as attachment_file:
                    attachment_file.write(email_content)  

                for i in range(4,len(email_content_list)-1 , 2):
                    attachmentName = getAttachmentName(email_content_list[i])
                    path_attachment = os.path.join(pathMessage,attachmentName)
                    with open(path_attachment, 'wb') as attachment_file:
                        attachment_file.write(base64.b64decode(email_content_list[i+1]))   
                        #print(f"Attachment saved: {attachmentName}")
                
        # Quit the session
        pop_conn.sendall(b'QUIT\r\n')
        response = pop_conn.recv(1024).decode()
        #print(response)

# # Set your POP3 server details

# pop3_username = 'qknetwork41@gmail.com'
# pop3_password = '25092004'  # Consider using app-specific password for security

# Call the retrieve_email_with_attachment_socket function
# retrieve_email_with_attachment_socket( pop3_username, pop3_password)

