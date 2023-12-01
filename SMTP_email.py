import base64
import socket
import os
def recipient_list_to_message(recipient_email_list):
    message=''
    for recipient_email in recipient_email_list:
        message+=recipient_email+', '
    message=message[0:len(message)-2]
    return message
def send_email_with_attachment(sender_email, to_email_list, subject, body, attachment_paths, smtp_host, smtp_port,cc_email_list=''):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the SMTP server
        client_socket.connect((smtp_host, smtp_port))
        response = client_socket.recv(1024).decode()

        # Send EHLO command
        client_socket.sendall(b'EHLO example.com\r\n')
        response = client_socket.recv(1024).decode()

        # Send MAIL FROM command
        client_socket.sendall(f'MAIL FROM: <{sender_email}>\r\n'.encode())
        response = client_socket.recv(1024).decode()

        # Send RCPT TO command
        for to_email in to_email_list:  
            client_socket.sendall(f'RCPT TO: <{to_email}>\r\n'.encode())
            response = client_socket.recv(1024).decode()

        for cc_email in cc_email_list:  
            client_socket.sendall(f'RCPT TO: <{cc_email}>\r\n'.encode())
            response = client_socket.recv(1024).decode()
            
        # Send DATA command
        client_socket.sendall(b'DATA\r\n')
        response = client_socket.recv(1024).decode()
        
        # Construct the email message with attachment
        to_email_message=recipient_list_to_message(to_email_list)
        cc_email_message=recipient_list_to_message(cc_email_list)
        email_message = (
            f'Subject: {subject}\r\n'
            f'From: {sender_email}\r\n'
            f'To: {to_email_message}\r\n'
        )
        if(cc_email_list!=''):
            email_message+=f'Cc: {cc_email_message}\r\n'
        email_message+=(
            f'MIME-Version: 1.0\r\n'
            f'Content-Type: multipart/mixed; boundary=my_boundary\r\n'
            f'--my_boundary\r\n'
            f'Content-Type: text/plain; charset="utf-8"\r\n'
            f'{body}\r\n\r\n'
            f'--my_boundary\r\n'
            f'Content-Type: application/octet-stream\r\n'
        )
        # Read attachment file and encode in base64
        for attachment_path in attachment_paths:
            email_message+= f'Content-Disposition: attachment; filename="{os.path.basename(attachment_path)}"\r\n\r\n'
            with open(attachment_path, 'rb') as attachment_file:
                attachment_data = base64.b64encode(attachment_file.read()).decode('utf-8')
        
            chunk_size = 1024  # Adjust the chunk size as needed
            for i in range(0, len(attachment_data), chunk_size):
                chunk = attachment_data[i:i + chunk_size]
                email_message += f'{chunk}\r\n'
            email_message+='--my_boundary\r\n'
        # # Add attachment data to the email message
        # email_message += f'{attachment_data}\r\n\r\n'

        # End the email message
        email_message += '--my_boundary--\r\n.\r\n'

        # Send the email message
        client_socket.sendall(email_message.encode())
        response = client_socket.recv(1024).decode()

        # Send QUIT command
        client_socket.sendall(b'QUIT\r\n')
        response = client_socket.recv(1024).decode()

# # # Set your email server details
# smtp_host = 'localhost'  # Assuming the server is running on the same machine
# smtp_port = 2225  # Use the port your test mail server is using (2225 in your case)

# # # Set email details
# sender_email = 'nguyenquangkhai2509@gmail.com'
# to_email_list = ['nguyenquangkhai2509@gmail.com']
# cc_email_list = ['cclemon@gmail.com']
# subject = 'Test Email with Attachment'
# body = 'This is a test email with an attachment sent from Python.'
# attachment_paths = ["D:\Modem.txt","D:\Socket\cmd.txt"]     # Replace with the actual path to your file

# # Call the send_email_with_attachment function
# send_email_with_attachment(sender_email, to_email_list, subject, body, attachment_paths, smtp_host, smtp_port,cc_email_list)
