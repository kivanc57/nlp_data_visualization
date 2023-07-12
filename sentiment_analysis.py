import os.path
import re
import matplotlib.pyplot as plt
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')


def read_texts(file_directory, mode="r", encoding="utf-8"):
    with open( file_directory ) as text:
        text_data = text.read()
        text_data = re.sub("\n\n", " ", text_data)
    
    return text_data


def analyse_sentiment(text_data):
    sent_scores = []
    text_data = nlp(text_data)
    for sent in text_data.sents:
        sentiment = sent._.blob.polarity
        sentiment = round(sentiment,2)
        sent_scores.append(sentiment)
    return sent_scores

def make_chart(sent_scores, output_directory, file_name):
    xAxis = [y for y in range(len(sent_scores))]
    plt.plot(xAxis,sent_scores, color='red', marker='o')
    plt.title('Sentiment Score Chart', fontsize=14)
    plt.xlabel('Sentence Index', fontsize=14)
    plt.ylabel('Sentiment Scores', fontsize=14)
    plt.grid(True)
    plt.show()
    plt.savefig(output_directory + str(file_name))


def main(input_directory, output_directory, file_name):
    read = read_texts(input_directory)
    analysed = analyse_sentiment(read)
    make_chart(analysed, output_directory, file_name)

if (__name__ == "__main__"):
    file_directory = os.path.expanduser(r"/Users/admin/Desktop/Workplace/Data/news_sample.txt")
    output_directory = os.path.expanduser(r"/Users/admin/Desktop/")
    file_name = "sentiment_chart.png"
    main(file_directory, output_directory, file_name)