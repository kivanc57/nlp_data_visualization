import os.path
import re

def extract_mails(file_directory):
    mails = []
    with open( file_directory, mode="r", encoding="utf-8") as text:
        for line in text:
            identified_emails = re.findall(r"\w+@\w+\.\w+", line)
            for email in identified_emails:
                mails.append(email)
                if len(mails) % 100 == 0:
                    print(len(mails))
                    
    return mails


#Print the results
def print_mails(mails):
    for mail in mails:
        print(mail)

def main(file_directory):
    mail_list = extract_mails(full_path)
    print_mails(mail_list)

if (__name__ == "__main__"):
    full_path = os.path.expanduser(r"/Users/admin/Desktop/text.txt")
    main(full_path)
