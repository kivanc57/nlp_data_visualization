import xml.etree.ElementTree as ET

# Get an iterable.
def extract_viruses(file_name):
    virus_descriptions = {}
    virus = ""
    key = ""
    evidence = ""

    accession = r'{http://uniprot.org/uniprot}accession'
    function = r'{http://uniprot.org/uniprot}comment type="function"'

    for event, el in ET.iterparse(file_name):
        if event == "start":
            if el.tag == accession:
                key = el.text
                virus_descriptions[key] = ""

        if event == "end":
            if el.tag == function:
                text = el.find("text").text
                virus_descriptions[key] = text
                virus = ""

        el.clear()
    return virus_descriptions


def write_data(file_name, virus_descriptions):
    with open(file_name, mode="w+", encoding="utf-8") as new_text:
        for virus in virus_descriptions.keys():
            new_line = virus + "\t" + virus_descriptions[virus] + "\n"
            new_text.write(new_line)


if __name__ == '__main__':
    file_name = r"/Users/admin/Desktop/Workplace/Data/P0DTC2.xml"
    virus_descriptions = extract_viruses(file_name)
    write_data(file_name + ".txt", virus_descriptions)
