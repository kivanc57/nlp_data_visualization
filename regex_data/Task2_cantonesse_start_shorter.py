import os.path
import re

def read_text(file_directory):
    with open( file_directory, mode="r", encoding="utf-8" ) as text:
        text_data = text.read()
    
    return text_data


def extract_patterns(text_data):

    cantonesse_expression = u'[\u4e00-\u9fff]{2}'
    cantonesse_characters = re.findall (cantonesse_expression, text_data)
#More info about the chinese detection:
#https://stackoverflow.com/questions/2718196/find-all-chinese-text-in-a-string-using-python-and-regex


    middle_element = re.findall(r"([aA-zZ]+\d(\s[aA-zZ]+\d)*)", text_data)

    count = 0
    for el in middle_element:
        el = el[0]
        middle_element[count] = el
        count += 1


    last_element = re.findall(r"\d+-\w", text_data)


    extracted_data = {
        "cantonesse_characters" :   cantonesse_characters,
        "middle_element"        :   middle_element,
        "last_element"          :   last_element
    }


    return extracted_data


def edit_middle_element(extracted_data):
    new_el = ""
    count = 0

    for el in extracted_data["middle_element"]:
        numbers = re.findall(r"\d", el)
        for number in numbers:
            new_el += (number + "\t")
        extracted_data["middle_element"][count] =  new_el
        count += 1

    return extracted_data
        


def write_data(extracted_data):
    count = 0

    with open(r"/Users/admin/Desktop/editedText.txt", mode="w+", encoding="utf-8") as new_text:
            for el in extracted_data["last_element"]:
                
                line = extracted_data["cantonesse_characters"][count]     + "\t" +\
                       extracted_data["middle_element"][count]            +\
                       extracted_data["last_element"][count][-1]          + "\n"

                new_text.write(line)
                count += 1


def main(file_directory):
    read = read_text(full_path)
    extracted = extract_patterns(read)
    edited = edit_middle_element(extracted)
    written = write_data(edited)
    written

if (__name__ == "__main__"):
    file_directory = os.path.expanduser(r"/Users/admin/Desktop/text.txt")
    main(file_directory)