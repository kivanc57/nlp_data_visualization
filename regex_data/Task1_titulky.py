import os.path
import re

def read_text(file_directory):
    with open( file_directory, mode="r", encoding="utf-8" ) as text:
        text_data = text.read()
    
    return text_data


def split_data(text_data):
    lines = {}
    

    dates = re.findall(r"\d{1,2}.\s\w+\s+\d{4}", text_data)
    times = re.findall(r"\b\d{0,2}\:\d{0,2}\b", text_data)
    messages = re.findall(r"^([A-Z]+|[ŇÓŘŠÚŮÝŽ])+.*\w|[ňóřšťúůýž]", text_data)

    
    lines["date"] = dates
    lines["time"] = times
    lines["message"] = messages

    return lines


def organise_dates(lines):
    count = 0

    for date in lines["date"]:
        date = re.split(". | ", date)
        day = date[0]
        month = date[1]
        year = date[-1]

        date = year + "\t" + month + "\t" + day
        lines["date"][count] = date
        count += 1

    return lines


def write_data(lines):
    count = 0
    with open('/Users/admin/Desktop/editedText.txt', mode="w+", encoding="utf-8") as new_text:
        for date in lines["date"]:
            new_line = lines["date"][count] + "\t" + lines["time"][count] + "\t" + lines["message"][count] + "\n"
            new_text.write(new_line)
            count += 1


def main(file_directory):

    read = read_text(file_directory)
    splitted = split_data(read)
    organised = organise_dates(splitted)
    written = write_data(organised)
    written


if (__name__ == "__main__"):
    file_directory = os.path.expanduser(r"/Users/admin/Desktop/text.txt")
    main(file_directory)