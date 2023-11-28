from SMTP_email import send_email_with_attachments
from path_handling import danh_sach_thu_muc
from path_handling import print_MessageList
from path_handling import print_message
from path_handling import check_attachmentFile
from path_handling import change_location_file
from path_handling import count_messageInFolder
from POP3_email import retrieve_email_with_attachment_socket




import os
class EmailClient:
    def __init__(self):
        self.inbox = []

    def send_email(self):
        to_addresses = input("To: ").split(', ')
        cc_addresses = input("CC: ").split(', ')
        bcc_addresses = input("BCC: ").split(', ')
        subject = input("Subject: ")
        content = input("Content: ")
        has_attachments = input("Có gửi kèm file (1. có, 2. không): ") == '1'
        attachments = []
        if has_attachments:
            num_attachments = int(input("Số lượng file muốn gửi: "))
            for i in range(num_attachments):
                attachment_path = input(f"Cho biết đường dẫn file thứ {i + 1}: ")
                attachments.append(attachment_path)
        send_email_with_attachments(sender_email,to_addresses,subject,content,attachments,smtp_host,cc_addresses)
        # for i in range(0,len(bcc_addresses)):
        #     send_email_with_attachments(sender_email,bcc_addresses[i],subject,content,attachments,smtp_host)
        # print("Đã gửi email thành công")

    def view_inbox(self):
        print("Đây là danh sách các folder trong mailbox của bạn: ")
        listFolder = danh_sach_thu_muc(r"D:\MailBox")
        for i in range(0,len(listFolder)):
            print(i+1,listFolder[i])  

    def run(self):
        while True:
            print("\nVui lòng chọn Menu:")
            print("1. Để gửi email")
            print("2. Để xem danh sách các email đã nhận")
            print("3. Thoát")
            choice = input("Bạn chọn: ")
            if choice == '1':
                self.send_email()
                retrieve_email_with_attachment_socket(sender_email, password,pop3_host)
            elif choice == '2':
                self.view_inbox()
                choice = int(input("Bạn muốn xem email trong folder nào: "))
                listFolder = danh_sach_thu_muc(r"D:\MailBox")
                path_folder = os.path.join(r"D:\MailBox",listFolder[choice-1])

                if count_messageInFolder(path_folder) != 0:
                    print_MessageList(path_folder)
                    while True:
                        choice = input("Bạn muốn đọc Email thứ mấy: ")
                        if choice == 0 :
                            print_MessageList(path_folder)
                            continue
                        elif choice == '':
                            break
                        choice = int(choice)
                        print("Nội dung email của email thứ",choice)
                        path_message = print_message(path_folder,choice)
                        list_attachmentFile = check_attachmentFile(path_message)
                        if len(list_attachmentFile) != 0:
                            if input("Trong email này có attached file, bạn có muốn save không: ") == 'có':
                                destination_path = input("Cho biết đường dẫn bạn muốn lưu: ")
                                for path_file in list_attachmentFile:
                                    change_location_file(path_file,destination_path)
                                    print(f"Đã lưu file tại {destination_path}")          
                else:
                    print("Không có email nào trong folder này.")
                
            elif choice == '3':
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

if __name__ == "__main__":
    # sender_email =input("Nhập tên đăng nhập: ")
    # password =input("Nhập mật khẩu: ")
    sender_email ='qknetwork41@gmail.com'
    password ="khanh0401"
    smtp_host = 'localhost'
    pop3_host = 'localhost'
    email_client = EmailClient()
    email_client.run()
