import socket
import base64
import os

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
def list_email_name(pop_conn):
    pop_conn.sendall(b'UIDL\r\n')
    response=pop_conn.recv(1024).decode().split();
    uidl=[]
    for i in range(2,len(response)-1,2):
        uidl.append(response[i])
    return uidl
def retrieve_email_with_attachment(pop3_host, pop3_port, username, password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pop_conn:
        pop_conn.connect((pop3_host, pop3_port))

        response = pop_conn.recv(1024).decode()

        # Send user credentials
        pop_conn.sendall(f'USER {username}\r\n'.encode())
        response = pop_conn.recv(1024).decode()

        pop_conn.sendall(f'PASS {password}\r\n'.encode())
        response = pop_conn.recv(1024).decode()

        pop_conn.sendall(b'LIST\r\n')
        response = pop_conn.recv(1024).decode()

        num_messages = len(response.splitlines())-2

        email_name_list=list_email_name(pop_conn)

        for i in range(1, num_messages + 1):
            pop_conn.sendall(f'RETR {i}\r\n'.encode())
            email=''
            while response := pop_conn.recv(4096).decode():
                email+=response
                if response.find('--my_boundary--')!=-1:
                    break  
            email=email.replace('\r\n--my_boundary--','') 

            with open('D:\\Gmail\\'+username+'\\Inbox\\Unread\\'+email_name_list[i-1],'w') as file:
                file.write(email)
               
            
        # Quit the session
        pop_conn.sendall(b'QUIT\r\n')
        response = pop_conn.recv(1024).decode()

# # Set your POP3 server details
# pop3_host = 'localhost'
# pop3_port = 3335  # Standard POP3 port
# pop3_username = 'nguyenquangkhai2509@gmail.com'
# pop3_password = '25092004'  # Consider using app-specific password for security

# # # Call the retrieve_email_with_attachment_socket function
# retrieve_email_with_attachment(pop3_host, pop3_port, pop3_username, pop3_password)