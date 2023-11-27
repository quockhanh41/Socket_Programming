import base64
import socket
import os

def send_email_bcc_with_attachments(sender_email, recipient_email, subject, body, attachment_paths):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the SMTP server
        client_socket.connect(('localhost', 2225))
        response = client_socket.recv(1024).decode()
        #print(response)

        # Send EHLO command
        client_socket.sendall(b'EHLO example.com\r\n')
        response = client_socket.recv(1024).decode()
        #print(response)

        # Send MAIL FROM command
        client_socket.sendall(f'MAIL FROM: <{sender_email}>\r\n'.encode())
        response = client_socket.recv(1024).decode()
        #print(response)

        # Send RCPT TO command
        client_socket.sendall(f'RCPT TO: <{recipient_email}>\r\n'.encode())
        response = client_socket.recv(1024).decode()
        #print(response)

        # Send DATA command
        client_socket.sendall(b'DATA\r\n')
        response = client_socket.recv(1024).decode()
        #print(response)

        # Construct the email message with attachments
        email_message = (
            f'Subject: {subject}\r\n'
            f'From: {sender_email}\r\n'
            f'To: {recipient_email}\r\n\r\n'
            f'MIME-Version: 1.0\r\n'
            f'Content-Type: multipart/mixed; boundary=my_boundary\r\n\r\n'
            f'--my_boundary\r\n'
            f'Content-Type: text/plain; charset="utf-8"\r\n\r\n'
            f'{body}\r\n\r\n'
        )

        # Add attachments
        for attachment_path in attachment_paths:
            # Read attachment file and encode in base64
            with open(attachment_path, 'rb') as attachment_file:
                attachment_data = base64.b64encode(attachment_file.read()).decode('utf-8')

            # Check if the attachment size exceeds 3MB
            if len(attachment_data) > 3 * 1000 * 1000:
                print(f"Attachment {attachment_path} exceeds the 3MB size limit. Skipping.")
                continue

            # Add attachment data to the email message
            email_message += (
                f'\r\n--my_boundary\r\n'
                f'Content-Type: application/octet-stream\r\n'
                f'Content-Disposition: attachment; filename="{os.path.basename(attachment_path)}"\r\n\r\n'
            )

            chunk_size = 72  # Adjust the chunk size as needed
            for i in range(0, len(attachment_data), chunk_size):
                chunk = attachment_data[i:i + chunk_size]
                email_message += f'{chunk}\r\n'

        # End the email message
        email_message += '--my_boundary--\r\n.\r\n'

        # Send the email message
        client_socket.sendall(email_message.encode())
        response = client_socket.recv(1024).decode()
        #print(response)

        # Send QUIT command
        client_socket.sendall(b'QUIT\r\n')
        response = client_socket.recv(1024).decode()
        #print(response)

# send_email_bcc_with_attachments(
#     sender_email= "qknetwork41@gmail.com",
#     recipient_email="qknetwork41@gmail.com",
#     subject="Subject of the email",
#     body="Body of the email",
#     attachment_paths=[ "D:\cmd.txt","D:\W06-Polymophism.pdf"]
# )
