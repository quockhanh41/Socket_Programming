from bcc import send_email_bcc_with_attachments
from to_cc import send_email_to_cc_with_attachments

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
            send_email_to_cc_with_attachments(sender_email,to_addresses,cc_addresses,subject,content,attachments)
            for i in range(0,len(bcc_addresses)):
                    send_email_bcc_with_attachments(sender_email,bcc_addresses[i],subject,content,attachments)
            print("Đã gửi email thành công")

    def view_inbox(self):
        print("Đây là danh sách email trong Inbox folder")
        for i, email in enumerate(self.inbox, start=1):
            print(f"{i}. {email.sender}, {email.subject}")

    def read_email(self, index):
        email = self.inbox[index - 1]
        print(f"Nội dung email của email thứ {index}:")
        print(email.content)

        if email.attachments:
            save_attachments = input("Trong email này có attached file, bạn có muốn save không: ").lower() == 'có'
            if save_attachments:
                for i, attachment in enumerate(email.attachments, start=1):
                    save_path = input(f"Cho biết đường dẫn bạn muốn lưu file thứ {i}: ")
                    # Lưu file tại đường dẫn save_path
                    print(f"Đã lưu file {attachment} tại {save_path}")

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
                self.view_inbox()
                folder_choice = input("Bạn muốn xem email trong folder nào: ")
                if folder_choice == '':
                    continue
                folder_index = int(folder_choice)
                if 1 <= folder_index <= len(self.inbox):
                    self.read_email(folder_index)
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
    email_client = EmailClient()
    email_client.run()
