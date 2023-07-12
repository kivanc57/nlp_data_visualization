import os.path
from matplotlib import pyplot as plt
import spacy

nlp = spacy.load('en_core_web_sm')

def get_NLP_texts(file_path):
    with open( file_path, mode="r", encoding="utf-8") as text:
        doc = nlp(text.read())
    
    return doc


def get_sent_length( doc ):
    sents = [len(sent) for sent in doc.sents]
    total = sum(sents)
    average = total / len(sents)

    data ={
        "average_length" : average,
        "sent_lengths" : sents,
    }
    return data


def save_histogram( data, output_directory ):
    sents = data["sent_lengths"]
    sent_amount = len(sents)
    plt.hist(sents, edgecolor='black')
    plt.xlabel("Token Amount")
    plt.ylabel("Sentence Amount")
    plt.savefig(output_directory + r"english_histogram.png")


def main(input_directory, output_directory):
    read = get_NLP_texts(input_directory)
    gotten = get_sent_length(read)
    save_histogram(gotten, output_directory)

if (__name__ == "__main__"):
    input_directory = os.path.expanduser(r"/Users/admin/Desktop/Workplace/EN2.txt")
    output_directory = os.path.expanduser(r"/Users/admin/Desktop/")
    main(input_directory, output_directory)
