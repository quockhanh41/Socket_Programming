from SMTP_email import send_email_with_attachment
from POP3_email import retrieve_email_with_attachment
from path_handling import*
import shutil
class EmailClient:
    def __init__(self):
        self.inbox = []
    def send_email(self):
        to_addresses = input("To: ").split(', ')
        cc_addresses = input("Cc: ").split(', ')
        bcc_addresses = input("Bcc: ").split(', ')
        if to_addresses[0]!='':
            for to_address in to_addresses:
                create_user_folder(to_address)
        if cc_addresses[0]!='':
            for cc_address in cc_addresses:
                create_user_folder(cc_address)
        if bcc_addresses[0]!='':
            for bcc_address in bcc_addresses:
                create_user_folder(bcc_address)
        subject = input("Subject: ")
        content = input("Content: ")
        has_attachments = input("Có gửi kèm file (1. Có, 2. Không): ") == '1'
        attachments = []
        if has_attachments:
            num_attachments = int(input("Số lượng file muốn gửi: "))
            for i in range(num_attachments):
                attachment_path = input(f"Cho biết đường dẫn file thứ {i + 1}: ")
                attachments.append(attachment_path)
        send_email_with_attachment(sender_email,to_addresses,subject,content,attachments,'localhost',2225,cc_addresses)
        for i in bcc_addresses:
            i=[i]
            send_email_with_attachment(sender_email,i,subject,content,attachments,'localhost',2225)

    def run(self):
        while True:
            print("\nVui lòng chọn Menu:")
            print("1. Để gửi email")
            print("2. Để xem danh sách các email đã nhận")
            print("3. Thoát")
            choice = input("Bạn chọn: ")
            if choice == '1':
                self.send_email()
            elif choice == '2':
                retrieve_email_with_attachment('localhost',3335,sender_email, password)
                folder=["Inbox","Project","Important","Work","Spam"]
                print("Đây là danh sách các folder trong mailbox của bạn")
                print("1. Inbox")
                print("2. Project")
                print("3. Important")
                print("4. Work")
                print("5. Spam")
                choice1 = int(input("Bạn muốn xem email trong folder nào: "))
               
                while True:
                    unread_file_list=getFileList(f'D:\\Gmail\\{sender_email}\\{folder[choice1-1]}\\Unread')
                    read_file_list=getFileList(f'D:\\Gmail\\{sender_email}\\{folder[choice1-1]}\\Read')
                    printMsgList(unread_file_list,sender_email,choice1,'Unread')
                    printMsgList(read_file_list,sender_email,choice1,'Read')
                    choice2 = input("Bạn muốn đọc Email thứ mấy: ")
                    if choice2 == 0 :
                        printMsgList(unread_file_list,sender_email,choice1,'Unread')
                        printMsgList(read_file_list,sender_email,choice1,'Read')
                        continue
                    elif choice2 == '':
                        break
                    choice2 = int(choice2)
                    print("Nội dung email của email thứ",choice2) 
                    if(choice2<=len(unread_file_list)): 
                        email,file_list=getEmail(f'D:\\Gmail\\{sender_email}\\{folder[choice1-1]}\\Unread\\{unread_file_list[choice2-1]}')
                        print(email)
                        email=email.split('\r\n')
                        if(email[len(email)-1].find('File: ')!=-1):
                            print("Trong email này có attached file, bạn có muốn save không: 1.Có 2.Không")
                            choice3=input("Lựa chọn của bạn: ")
                            if(choice3==1):
                                path=input("Cho biết đường dẫn bạn muốn lưu: ")
                                for file in file_list:
                                    downloadFile(file,path)
                    shutil.move(f'D:\\Gmail\\{sender_email}\\{folder[choice1-1]}\\Unread\\{unread_file_list[choice2-1]}', f'D:\\Gmail\\{sender_email}\\{folder[choice1-1]}\\Read\\{unread_file_list[choice2-1]}')
                else:
                    print("Không có email nào trong folder này.")         
            elif choice1 == '3':
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

if __name__ == "__main__":
    # sender_email =input("Nhập tên đăng nhập: ")
    # password =input("Nhập mật khẩu: ")
    create_folder("D:\Gmail")
    sender_email ='nguyenquangkhai2509@gmail.com'
    password ="khanh0401"
    email_client = EmailClient()
    email_client.run()