from xml.etree.ElementTree import iterparse
from pandas import DataFrame
import matplotlib.pyplot as plt
from seaborn import barplot
import logging

#Load configs
from config.common_config import get_join_path, basename, configure_logging
from config.constants import FOLDER_NAMES

#Configure logging
script_name = basename(__file__)[:-3]
configure_logging(script_name)
logger = logging.getLogger(__name__)


def get_list_xml(source, tag, events = ('start', 'end')):
    context = iterparse(source, events)
    tags_list = list()
    namespace = None

    try:
        for event, el in context:
            if namespace is None and el.tag.startswith('{'):
                namespace = el.tag[1:el.tag.find('}')]
            if namespace and el.tag == f'{{{namespace}}}{tag}':
                    tags_list.append(el.text)
            el.clear()
        logger.info(f"Extraction succeeded: {source}")
        return tags_list
    
    except Exception as e:
        logger.exception(f"Extraction failed: {e} in {source}")
        return None

def write_txt(destination, input_list):
    try:
        with open(destination, mode='w+', encoding='utf-8', errors='replace', newline='') as f:
            for el in input_list:
                if el:
                    f.write(f'{el}\n')
        logger.info(f"Writing succeeded: {destination}")

    except Exception as e:
        logger.exception(f"Writing failed: {e} in {destination}")
        return None
    
def get_frequency_list(word_list):
    frequency_dict = dict()

    try:
        for word in word_list:
            frequency_dict[word] = frequency_dict.get(word, 0) + 1
        logger.info("Created frequency list")
        return frequency_dict
    
    except Exception as e:
        logger.exception(f"Failed frequency list: {e}")

def get_bar_plot(destination, frequency_dict, x_name, y_name, top_n=10, title=None, palette='viridis'):
    try:
        df = DataFrame(frequency_dict.items(), columns=[x_name, y_name])
        df_sorted = df.sort_values(by=y_name, ascending=False).head(top_n)

        plt.figure(figsize=(12, 8))
        barplot(x=x_name, y=y_name, data=df_sorted, palette=palette, hue=x_name, legend=False)
        plt.xlabel = x_name
        plt.ylabel = y_name
        plt.title(title, fontweight = "bold")

        plt.savefig(destination)
        plt.close()
        logger.info(f"Graph created in {destination}")

    except Exception as e:
        logger.exception(f"Graph failed: {e} in {destination}")

def main():
    try:
        input_folder_name, output_folder_name = FOLDER_NAMES['input_folder_name'], FOLDER_NAMES['output_folder_name']
        input_xml_name = 'faust_2010_07_es_01.treex.xml'
        output_file_name = 'lemmas.txt'
        output_graph_name = 'bar_chart.png'
        tag = 'lemma'

        source = get_join_path(input_folder_name, input_xml_name, is_sample=True)
        destination_xml = get_join_path(output_folder_name, output_file_name, is_sample=True)
        destination_graph = get_join_path(output_folder_name, output_graph_name, is_sample=True)

        mail_list = get_list_xml(source, tag, events = ('start', 'end'))
        write_txt(destination_xml, mail_list)
        frequency_dict = get_frequency_list(mail_list)
        get_bar_plot(destination_graph, frequency_dict, x_name='Frequency', y_name='Lemma', top_n=10, title='Frequency Distribution of Lemmas')


        logger.info(f"Successfully executed: {basename(__file__)}")

    except Exception as e:
        logger.exception(f"Error occurred in main function: {e} in {basename(__file__)}")

if __name__ == '__main__':
    main()
