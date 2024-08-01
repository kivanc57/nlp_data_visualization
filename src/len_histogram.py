from spacy import load
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


def get_doc(source):
    try:
        with open(source, mode='r', encoding='utf-8', errors='replace') as f:
            doc = nlp(f.read())
        logger.info(f"Extraction succeeded: {source}")
        return doc
    
    except Exception as e:
        logger.error(f"Extraction failed: {e} in {source}")
        return None

def get_sentence_lengths(doc):
    try:
        sent_lengths = [len(sent) for sent in doc.sents]
        logger.info(f"List created")
        return sent_lengths
    except Exception as e:
        logger.exception(f"List failed: {e}")
        return None 

def get_histogram(data, destination, color = 'red', bins=20,
                    x_label = 'Sentence Length', y_label ='Number of Sentences',
                    graph_name='histogram.png', title="Distribution of Sentence Lengths"):
    try:
        plt.hist(data, edgecolor='black', histtype='bar', bins=bins, color=color, alpha=0.7, density=1)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title("Distribution of Sentence Lengths", fontweight = "bold")
        plt.savefig(destination)
        logger.info(f"Graph: {graph_name} created in {destination}")

    except Exception as e:
        logger.exception(f"Graph: {graph_name} failed: {e} in {destination}")
        return None

def main():
    try:
        input_folder_name, output_folder_name = FOLDER_NAMES['input_folder_name'], FOLDER_NAMES['output_folder_name']
        input_file_name = 'EN2.txt'
        output_file_name = 'histogram.png'
        source = get_join_path(input_folder_name, input_file_name, is_sample=True)
        destination = get_join_path(output_folder_name, output_file_name, is_sample=True)

        doc = get_doc(source)
        sentence_lengths = get_sentence_lengths(doc)
        get_histogram(sentence_lengths, destination, color = 'red', bins=20,
                    x_label = 'Sentence Length', y_label ='Number of Sentences',
                    graph_name='histogram.png', title="Distribution of Sentence Lengths")
        logger.info(f"Successfully executed: {basename(__file__)}")

    except Exception as e:
        logger.exception(f"Error in main function: {e}")

if __name__ == '__main__':
    main()
