import os.path
import re

def read_text(file_directory):
    with open( file_directory, mode="r", encoding="utf-8" ) as text:
        text_data = text.read()
    
    return text_data


def extract_hashtags(text_data):
    hashtags = re.findall("#\w+", text_data)
    return hashtags


def write_data(hashtags):

    with open(r"/Users/admin/Desktop/editedText.txt", mode="w+", encoding="utf-8") as new_text:
        for hashtag in hashtags:
            new_text.write(hashtag + "\t")


def main(full_path):
    read = read_text(full_path)
    extracted = extract_hashtags(read)
    written = write_data(extracted)
    written

if (__name__ == "__main__"):
    file_directory = os.path.expanduser(r"/Users/admin/Desktop/text.txt")
    main(file_directory)