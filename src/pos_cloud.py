from os import listdir
from os.path import join
from bs4 import BeautifulSoup
from spacy import load
import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import logging

#Load configs
from config.common_config import get_join_path, basename, configure_logging
from config.constants import FOLDER_NAMES

#Load language modal
nlp = load('en_core_web_sm')

#Configure logging
script_name = basename(__file__)[:-3]
configure_logging(script_name)
logger = logging.getLogger(__name__)


def get_sgms(source):
    texts = []

    try:
        for file_name in listdir(source):
            if file_name.endswith('.sgm'):
                logging.info(f"File read: {file_name}")         
                file_path = join(source, file_name)
                try:
                    with open(file_path, mode='r', encoding='utf-8', errors='replace') as f:
                        data_file = f.read()
                        soup = BeautifulSoup(data_file, 'html.parser')
                        contents = soup.find_all('title')
                        texts.extend(content.get_text() for content in contents)
                
                except Exception as e:
                    logger.exception(f"Reading failed: {e} in {file_path}")
                    return None

        logging.info(f"Extraction succeeded: {source}")
        return texts
    
    except Exception as e:
        logger.exception(f"Extraction failed: {e} in {source}")
        return None

def get_docs(texts):
    try:
        return [nlp(text) for text in texts]
    
    except Exception as e:
        logger.exception(f"Failed to parse the document: {e}")
        return None

def detect_pos(titles, output_limit=100):
    verbs = dict()
    subjects = dict()
    objects = dict()

    try:
        for title in titles:
            for token in title:
                if token.is_alpha:
                    if token.pos_ == "VERB":
                        verbs[token.lemma_] = verbs.get(token.lemma_, 0) + 1
                    elif token.dep_ in ('nsubj', 'nsubjpass', 'ccomp', 'attr'):
                        subjects[token.lemma_] = subjects.get(token.lemma_, 0) + 1
                    elif token.dep_ in ('dobj', 'iobj', 'pobj'):
                        objects[token.lemma_] = objects.get(token.lemma_, 0) + 1

        sorted_verbs = dict(list(sorted(verbs.items(), key=lambda item:item[1], reverse=True))[:output_limit])
        sorted_subjects = dict(list((sorted(subjects.items(), key=lambda item:item[1], reverse=True)))[:output_limit])
        sorted_objects = dict(list(sorted(objects.items(), key=lambda item:item[1], reverse=True))[:output_limit])
        logger.info(f"POS parsing successful")
        return sorted_verbs, sorted_subjects, sorted_objects

    except Exception as e:
        logger.exception(f"Failed parsing POS: {e}")
        return None

def write_csv(destination, verbs_dict, subjects_dict, objects_dict):
    try:
        with open(destination, mode='w+', encoding='utf-8', errors='replace', newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                writer.writerow(['verb', 'verb_count', 'subject', 'subject_count', 'object', 'object_count'])
                for (verb, verb_count), (subj, subj_count), (obj, obj_count) in zip(verbs_dict.items(), subjects_dict.items(), objects_dict.items()):  
                        writer.writerow([verb, verb_count, subj, subj_count, obj, obj_count])
        logger.info(f"Writing succeeded: {destination}")

    except Exception as e:
        logger.exception(f"Failed writing: {e} in {destination}")
        return None
    
def get_word_cloud(destination, word_counts, title=None):
    try:
        wordcloud = WordCloud(
            width=800,height=800,
            background_color='white',
            min_font_size=10
            ).generate_from_frequencies(word_counts)
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title, fontweight = "bold")
        plt.savefig(destination)
        plt.close()
        logger.info(f"Graph created in {destination}")

    except Exception as e:
        logger.exception(f"Failed graph: {e} in {destination}")

def main():
    try:
        input_folder_name, output_folder_name = FOLDER_NAMES['input_folder_name'], FOLDER_NAMES['output_folder_name']
        input_file_name = 'reuters21578'
        output_csv_name = 'most10.csv'
        output_graph_name = 'word_cloud.png'

        source = get_join_path(input_folder_name, input_file_name, is_sample=True)
        destination_csv = get_join_path(output_folder_name, output_csv_name, is_sample=True)
        destination_graph = get_join_path(output_folder_name, output_graph_name, is_sample=True)

        texts = get_sgms(source)
        docs = get_docs(texts)
        verbs_dict, subject_dict, objects_dict = detect_pos(docs, output_limit=10)
        get_word_cloud(destination_graph, verbs_dict, title=None)
        write_csv(destination_csv, verbs_dict, subject_dict, objects_dict)
        logger.info(f"Successfully executed: {basename(__file__)}")

    except Exception as e:
        logger.exception(f"Error in main function: {e} in {basename(__file__)}")

if __name__ == '__main__':
    main()
