import xml.etree.ElementTree as ET

# Get an iterable.
def extract_lemmas(context):
    lemmas = []

    for index, (event, el) in enumerate(context):
        # Get the root element.
        if (index == 0):
            root = el

        if (el.tag == r'{http://ufal.mff.cuni.cz/pdt/pml/}lemma'):
            lemmas.append(el.text)
            root.clear()
    return lemmas

def write_lemmas(file_path, lemmas):
    with open(file_path, mode="w+", encoding="utf-8") as new_text:
        for lemma in lemmas:
            new_text.write(lemma + "\n")

def main(context):
    lemmas =extract_lemmas(context)
    write_lemmas("/Users/admin/Desktop/lemmas.txt", lemmas)

if (__name__ == "__main__"):
    context = ET.iterparse(r"/Users/admin/Desktop/Workplace/Data/faust_2010_07_es_01.treex.xml", events=("start", "end"))
    main(context)