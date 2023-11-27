import os
import shutil

def danh_sach_thu_muc(duong_dan):
    danh_sach_thu_muc = []
    for ten in os.listdir(duong_dan):
        duong_dan_day_du = os.path.join(duong_dan, ten)
        if os.path.isdir(duong_dan_day_du):
            danh_sach_thu_muc.append(ten)
    return danh_sach_thu_muc

def danh_sach_tap_tin(duong_dan):
    danh_sach_tap_tin = []
    for ten in os.listdir(duong_dan):
        danh_sach_tap_tin.append(ten)
    return danh_sach_tap_tin
def path_message(path_folder):
    amount_message_cur = len(danh_sach_thu_muc(path_folder))
    newFolder = 'Message ' + str(amount_message_cur +1 ) 
    path_newFolder = os.path.join(path_folder,newFolder) 
    if not os.path.exists(path_newFolder):
        os.makedirs(path_newFolder)
    return path_newFolder

# 1 tin nhắn có thể nằm trong nhiều chủ đề     
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

def print_readMessageList(path_folder,i):
    fileList = danh_sach_tap_tin(path_folder)
    subjectFile=''
    for path in fileList:
        if path.find('.') == -1: 
            #vì tên file không dc đặt có dấu '.' 
            #nên file không có dấu '.' là file subject
            subjectFile = path
            break
    # read() file subject và print
    path_subjectFile = os.path.join(path_folder,subjectFile)
    with open(path_subjectFile, 'r') as subject_file:
        content = subject_file.read()
        subject = content[content.find('Subject: ')+9:content.find('From: ')-2]
        sender = content[content.find('From: ')+6:content.find('To: ')-2]
        print(str(i)+'.',sender,subject)

def print_unreadMessageList(path_folder,i):
    fileList = danh_sach_tap_tin(path_folder)
    subjectFile=''
    for path in fileList:
        if path.find('.') == -1:
            subjectFile = path
            break
    path_subjectFile = os.path.join(path_folder,subjectFile)
    with open(path_subjectFile, 'r') as subject_file:
        content = subject_file.read()
        subject = content[content.find('Subject: ')+9:content.find('From: ')-2]
        sender = content[content.find('From: ')+6:content.find('To: ')-2]
        print(str(i)+'. (chưa đọc)',sender,subject)
    
def count_messageInFolder(path_folder):
    count = 0
    path_read = os.path.join(path_folder,"Read")
    count += len(danh_sach_tap_tin(path_read))
    path_unread = os.path.join(path_folder,"Unread")
    count += len(danh_sach_tap_tin(path_unread))
    return count

# hiện trạng thái tn, ng gửi và subject tất cả các tin nhắn 
# và trả lại đường dẫn tin nhắn muốn mở 
def print_MessageList(path_folder):
    path_read = os.path.join(path_folder,"Read")
    read_list = danh_sach_thu_muc(path_read)
    i = 1
    for messageFolder in read_list:
        path_messageFolder = os.path.join(path_read,messageFolder)
        print_readMessageList(path_messageFolder,i)
        i+=1
    path_unread = os.path.join(path_folder,"Unread")
    unread_list = danh_sach_thu_muc(path_unread)
    for messageFolder in unread_list:
        path_messageFolder = os.path.join(path_unread,messageFolder)
        print_unreadMessageList(path_messageFolder,i)
        i+=1

#in nội dung tin nhắn thứ index
def print_message(path_folder,index): 
    path_read = os.path.join(path_folder,"Read")
    read_list = danh_sach_thu_muc(path_read)
    path_unread = os.path.join(path_folder,"Unread")
    unread_list = danh_sach_thu_muc(path_unread)
    if(index<=len(read_list)):
        path_message = os.path.join(path_read,read_list[index-1])
    else: path_message = os.path.join(path_unread,unread_list[index-1-len(read_list)])
    fileList = danh_sach_tap_tin(path_message)
    subjectFile=''
    for fileName in fileList:
        if fileName.find('.') == -1: 
            subjectFile = fileName
            break
    path_subjectFile = os.path.join(path_message,subjectFile)
    with open(path_subjectFile, 'r') as subject_file:
        print(subject_file.read())
    return path_message

#kiểm tra message có tập đính kèm hay không 
def check_attachmentFile(path_message):
    attachmentList = []
    fileList = danh_sach_tap_tin(path_message)
    for fileName in fileList:
        if fileName.find('.') != -1: 
            path_attachmentFile = os.path.join(path_message,fileName)
            attachmentList.append(path_attachmentFile)
    return attachmentList

def change_location_file(source_path,destination_path):
    shutil.move(source_path, destination_path)
