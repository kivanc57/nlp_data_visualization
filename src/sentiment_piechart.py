from os import listdir
from os.path import join
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib.pyplot as plt
import logging

#Load configs
from config.common_config import get_join_path, basename, configure_logging
from config.constants import FOLDER_NAMES

#Configure logging
script_name = basename(__file__)[:-3]
configure_logging(script_name)
logger = logging.getLogger(__name__)


def get_texts(source):
    texts = []
    
    try:
        for file_name in listdir(source):
            if file_name.endswith('.sgm'):
                logger.info(f"Read: {file_name}")
                file_path = join(source, file_name)
                try:
                    with open(file_path, mode='r', encoding='utf-8', errors='replace') as f:
                        data_file = f.read()
                        soup = BeautifulSoup(data_file, 'html.parser')
                        contents = soup.find_all('title')
                        texts.extend(content.get_text() for content in contents)
                    logger.info(f"Reading succeeded in {source}")
                
                except Exception as e:
                    logger.exception(f"Reading failed: {e} in {source}")
                    return None

        logger.info(f"Extraction succeeded in {source}")
        return texts

    except Exception as e:
        logger.exception(f"Extraction failed: {e} in {source}") 
        return None

def get_sentiments(texts):
    sentiments = list()

    try:
        sentiments.extend(round(TextBlob(text).sentiment.polarity, 3) for text in texts)
        logger.info("Sentiments analysis succeeded")
        return sentiments
    
    except Exception as e:
        logger.exception(f"Sentiments analysis failed: {e}")
        return None

def categorize_sentiments(sentiments):
    try:
        sentiments_categorized = {
            'Positive': sum(s > 0 for s in sentiments),
            'Neutral': sum(s == 0 for s in sentiments),
            'Negative': sum(s < 0 for s in sentiments)
        }
        logger.info("Sentiment categorization succeeded")
        return sentiments_categorized

    except Exception as e:
        logger.exception(f"Sentiment categorization failed: {e}")
        return None

def get_pie_chart(destination, sentiments_categorized, title=None, graph_name='pie_chart.png'):
    try:
        plt.figure(figsize=(8, 8))
        plt.pie(
            sentiments_categorized.values(),
            labels=sentiments_categorized.keys(),
            autopct='%1.1f%%',
            colors=['#65d14f', '#66c2a5', '#c43737'],
            explode=(0.1, 0, 0),
            shadow=True,
            startangle=90
            )
        if title:
            plt.title(title, fontweight = "bold")
        plt.savefig(destination)
        logger.info(f"Pie chart: {graph_name} created in {destination}")
    
    except Exception as e:
        logger.error(f"Pie chart: {graph_name} failed: {e} in {destination}")
        return None

def main():
    try:
        input_folder_name, output_folder_name = FOLDER_NAMES['input_folder_name'], FOLDER_NAMES['output_folder_name']
        input_file_name = 'reuters21578'
        output_file_name = 'pie_chart.png'
        source = get_join_path(input_folder_name, input_file_name, is_sample=True)
        destination = get_join_path(output_folder_name, output_file_name, is_sample=True)

        text = get_texts(source)
        sentiments = get_sentiments(text)
        sentiments_categorized = categorize_sentiments(sentiments)
        get_pie_chart(destination, sentiments_categorized, title='Sentiment Distribution', graph_name='pie_chart.png')
        logger.info(f"Successfully executed: {basename(__file__)}")

    except Exception as e:
        logger.exception(f"Error in main function: {e}")

if __name__ == '__main__':
    main()
