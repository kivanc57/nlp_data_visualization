import os.path
import re

def read_text(file_directory):
    with open( file_directory, mode="r", encoding="utf-8" ) as text:
        text_data = text.read()
    
    return text_data


def split_data(text_data):
    edited_data = []
    lines = re.split("\n", text_data)
    for line in lines:
        new_line = re.split(r"[. |, |.]\s?", line)
        new_line.pop(-1)
        edited_data.append(new_line)

    return edited_data


def write_data(edited_data):
    with open('/Users/admin/Desktop/editedText.txt', mode="w+", encoding="utf-8") as new_text:

        for line in edited_data:

            data_to_write = {
                "first_name" : line[1],
                "second_name" : line[0],
                "birth_date" : line[2]
            }

            new_line = data_to_write["first_name"] + " " + data_to_write["second_name"] + ", " +  data_to_write["birth_date"] + "\n"
            new_text.write(new_line)



def main(file_directory):
    read = read_text(file_directory)
    splitted = split_data(read)
    written = write_data(splitted)
    written

if (__name__ == "__main__"):
    file_directory = os.path.expanduser(r"/Users/admin/Desktop/text.txt")
    main(file_directory)