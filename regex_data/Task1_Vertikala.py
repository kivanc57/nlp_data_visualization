import os.path
import re

def read_text(file_directory):
    with open( file_directory, mode="r", encoding="utf-8" ) as text:
        text_data = text.read()
    
    return text_data


def extract_patterns(text_data):
    expression = r"((\w+)|[ňóřšťúůýž]|[ŇÓŘŠÚŮÝŽ])(.*).\t[aA-Zz]"
    patterns = re.findall(expression, text_data)
    return patterns


def write_data(patterns):
    with open("newFile.txt", "w+") as new_text:
        for pattern in patterns:
            to_write = pattern[0] + "_" + pattern[-1] + "\t"
            new_text.write(pattern)


def main(file_directory):
    read = read_text(file_directory)
    extracted = extract_patterns(read)
    written = write_data(extracted)
    written

if (__name__ == "__main__"):
    file_directory = os.path.expanduser(r"/Users/admin/Desktop/text.txt")
    main(file_directory)