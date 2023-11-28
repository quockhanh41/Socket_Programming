from function_common import *
import mailsmtp 
import mailpop3 
import base64 

def content_choose1(list_mail, list_file, subject_mail, content_mail) :
    print("Day la thong tin soan email: (neu khong dien vui long nhan enter de bo qua)")
    
    # nhap thong in to,cc,bcc
    list_mail["to"] = input("To: ").replace(","," ").split()
    list_mail["cc"] = input("CC: ").replace(","," ").split()
    list_mail["bcc"] = input("BCC: ").replace(","," ").split()
    
    # nhap thong subject va content
    subject_mail = input("Subject: ")
    content_mail = input("Content: ")

    # nhap thong tin file 
    if (input("Co gui file (1.co, 2.khong): ") == "1") : 
        n = int(input("So luong file can gui: "))
        for i in range(1,n + 1): 
            print("Cho biet duong dan file thu ",end = "")
            list_file.append(input(f"{i}: ")) 

    return list_mail, list_file, subject_mail, content_mail  

def check_in_list(Listarray, key): 
    for i in Listarray: 
        if i == key: return True 
    return False

def Filter_mail(mail) : 
    Filter = readinfo_json("Filter")
    mailof_folder = {}
    mailof_folder["Inbox"] = []
    mailof_folder[Filter[0]["From-to"]] = []
    mailof_folder[Filter[1]["Subject-to"]] = []
    mailof_folder[Filter[2]["Content-to"]] = []
    mailof_folder[Filter[3]["Spam-to"]] = []

    for i in mail: 
        name_msg, From, subject, content, list_file = i 
        if check_in_list(Filter[0]["From"], From): mailof_folder[Filter[0]["From-to"]].append(i) 
        elif check_in_list(Filter[1]["Subject"], subject): mailof_folder[Filter[1]["Subject-to"]].append(i)  
        elif check_in_list(Filter[2]["Content"], content): mailof_folder[Filter[2]["Content-to"]].append(i)
        elif check_in_list(Filter[3]["Spam"], subject) or check_in_list(Filter[3]["Spam"], content): mailof_folder[Filter[3]["Spam-to"]].append(i) 
        else:
            mailof_folder["Inbox"].append(i)
    
    return mailof_folder 

def decode_base64_to_pdf(encoded_text, output_path):
    pdf_binary_data = base64.b64decode(encoded_text)
    with open(output_path, 'wb') as pdf_file:
        pdf_file.write(pdf_binary_data)
 
def content_choose2(list_folder, mailof_folder, readed_mail): 
    print("Day la danh sach cac mail trong folder cua ban: ")
    for i in range(0,len(list_folder)): print(f"{i + 1}. {list_folder[i]}")
    choose = input("Ban muon xem mail trong folder nao: ")
    if (choose == ""): return
    choose = int(choose)
    print("Day la danh sach trong " + list_folder[choose - 1] + " folder")
    pos = 0
    for i in mailof_folder[list_folder[choose - 1]]:
        name_msg, From, subject, content, list_file = i 
        pos = pos + 1
        print(pos,".",end = "")
        
        if (list_folder[choose - 1][pos - 1]) not in readed_mail: print("(chua doc)",end = "")
        print(f"<{From}>, <{subject}>")

    pos = input("Ban doc mail thu may: ")
    if (pos == ""): return 
    readed_mail[(list_folder[choose - 1],pos)] = True 
    pos = int(pos)
    name_msg, From, subject, content, list_file = mailof_folder[list_folder[choose - 1]][pos - 1]
    print(f"noi dung mail cua mail thu {pos} la: {content}")
    if (len(list_file) != 0):
        yn = input("Trong file co attached file, ban co muon save file khong (1.co, 2.khong): ")
        if (yn == "1"):
            path = input("cho biet duong dan muon luu: ")
            for i in list_file: 
                file_name,cont = i 
                outpath = path + file_name
                decode_base64_to_pdf(cont, outpath)
    

def MENU() :
    print("Vui long chon Menu: ")
    print("1. De gui email")
    print("2. De xem danh sach cac email da nhan")
    print("3. Thoat")
    choose = input("Ban chon: ")
    if (choose == "1"): 
        list_mail = {"to": [], "cc": [], "bcc": []}
        list_file = []
        subject_mail = content_mail = ""
        list_mail, list_file, subject_mail, content_mail = content_choose1(list_mail, list_file, subject_mail, content_mail)
        mailsmtp.client_mail(list_mail,list_file,subject_mail,content_mail)
    else:
        mail = mailpop3.received_mailserver()
        mailof_folder = Filter_mail(mail)
        list_folder = []
        for i in mailof_folder.keys(): list_folder.append(i)
        readed_mail = {}
        content_choose2(list_folder, mailof_folder, readed_mail)

    
if __name__ == "__main__":
    MENU()