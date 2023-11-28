from SMTP_email import send_email_with_attachment
from POP3_email import retrieve_email_with_attachment

import os
class EmailClient:
    def __init__(self):
        self.inbox = []
        
#Gmail->User->Mailbox->4 cai kia->Message
    def send_email(self):
        to_addresses = input("To: ").split(', ')
        cc_addresses = input("CC: ").split(', ')
        bcc_addresses = input("BCC: ").split(', ')
        subject = input("Subject: ")
        content = input("Content: ")
        has_attachments = input("Có gửi kèm file (1. Có, 2. Không): ") == '1'
        attachments = []
        if has_attachments:
            num_attachments = int(input("Số lượng file muốn gửi: "))
            for i in range(num_attachments):
                attachment_path = input(f"Cho biết đường dẫn file thứ {i + 1}: ")
                attachments.append(attachment_path)
            #Rut gon to_cc_bcc
        send_email_with_attachment(sender_email,to_addresses,subject,content,attachments,'localhost',2225,cc_addresses)
        for i in bcc_addresses:
            i=[i]
            send_email_with_attachment(sender_email,i,subject,content,attachments,'localhost',2225)
        print("Đã gửi email thành công")

    def run(self):
        while True:
            print("\nVui lòng chọn Menu:")
            print("1. Để gửi email")
            print("2. Để xem danh sách các email đã nhận")
            print("3. Thoát")
            choice = input("Bạn chọn: ")
            if choice == '1':
                self.send_email()
                retrieve_email_with_attachment('localhost',3335,sender_email, password)
              
            elif choice == '3':
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

if __name__ == "__main__":
    # sender_email =input("Nhập tên đăng nhập: ")
    # password =input("Nhập mật khẩu: ")
    sender_email ='nguyenquangkhai2509@gmail.com'
    password ="khanh0401"
    email_client = EmailClient()
    email_client.run()