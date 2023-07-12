import os
import re
from bs4 import BeautifulSoup
import spacy

def get_texts(input_directory, mode="r", encoding="utf-8"):
    docs = []
    for file_name in os.listdir(input_directory):
        if file_name.endswith(".sgm"):          
            file_path = os.path.join(str(input_directory), file_name)
            with open(file_path, mode='r', encoding='utf-8', errors='ignore') as f:
                data_file = f.read()
                
                soup = BeautifulSoup(data_file, 'html.parser')
                contents = soup.find_all('title')
                
                for content in contents:
                    docs.append(nlp(content.text))
    return docs


def analyse_Nentity_sentiments(new_titles):
    Nentity_sentiments = {}
    for sent, ent in zip(text_data.sents, text_data.ents):
        sentiment = sent._.blob.polarity
        sentiment = round(sentiment,2)
        entity = str(ent.text)
        Nentity_sentiments[entity] = sentiment
    return Nentity_sentiments


def write_table(Nentity_sentiments, output_directory):
    with open(output_directory,  mode="r", encoding="utf-8") as table:
        for entity in Nentity_sentiments:
            sentiment = Nentity_sentiments[entity]
            table.write(entity + "\t" + sentiment + "\n")


def main(input_directory, output_directory):
    text = get_texts(input_directory)
    dic = analyse_Nentity_sentiments(d)
    write_table(dic, output_directory)

if (__name__ == "__main__"):
    nlp = spacy.load('en_core_web_sm')
    input_directory = os.path.expanduser(r"/Users/admin/Desktop/Workplace/reuters21578")
    output_directory = os.path.expanduser(r"/Users/admin/Desktop/table_of_sentiments.txt")
    main(input_directory, output_directory)