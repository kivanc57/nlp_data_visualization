from xml.etree.ElementTree import iterparse
from json import dump
from spacy import load
from seaborn import color_palette
from spacy.lang.en.stop_words import STOP_WORDS
import matplotlib.pyplot as  plt
import squarify
import logging

#Load configs
from config.common_config import get_join_path, basename, configure_logging
from config.constants import FOLDER_NAMES

#Configure logging
script_name = basename(__file__)[:-3]
configure_logging(script_name)
logger = logging.getLogger(__name__)

#Load language modal
nlp = load('en_core_web_sm')

# Get an iterable.
def get_dict_xml(source, events=('start', 'end'), tags = ('accession', 'comment'),
                 attributes=(None, ('type', 'function'))):
    context = iterparse(source, events)
    tags_dict = dict()
    namespace = None
    key_el, text_el = None, None

    tag_1, tag_2 = tags
    try:
        for event, el in context:
            if namespace is None and el.tag.startswith('{'):
                namespace = el.tag[1:el.tag.find('}')]

            if namespace and el.tag == f'{{{namespace}}}{tag_1}':
                    if el.text and el.text.strip():
                        key_el = el.text.strip()

            if namespace and el.tag == f'{{{namespace}}}{tag_2}' and el.attrib.get(attributes[1][0]) == attributes[1][1]:
                    text_el = el.findtext(f'{{{namespace}}}text', '').strip()
                    if text_el:
                        if key_el in tags_dict.keys():
                            tags_dict[key_el] += " " + text_el
                        else:
                            tags_dict[key_el] = text_el
            el.clear()
        logger.info(f"Extraction succeeded: {source}")
        return tags_dict

    except Exception as e:
        logger.exception(f"Extraction failed: {e} in {source}")
        return None

def write_json(destination, data):
    try:
        with open(destination, mode='w+', encoding='utf-8', errors='replace', newline='') as f:
            dump(data, f, indent=4)
        logger.info(f"Writing succeeded: {destination}")

    except Exception as e:
        logger.exception(f"Error writing: {e} in {destination}")
        return None
    
def get_entity_dict(input_dict, nlp):
    entity_dict = dict()
    #Combined all the texts in values in one
    combined_text = ' '.join(map(str, input_dict.values()))

    try:
        for entitiy in nlp(combined_text).ents:
            entity_dict[entitiy.label_] = entity_dict.get(entitiy.label_, 0) + 1
        logger.info("Created entitiy dictionary")
        return entity_dict
    
    except Exception as e:
        logger.exception(f"Failed entity dictionary: {e}")
        return None
    
def get_treemap(destination, entity_dict, title='Distribution of Entity Labels'):
    try:
        labels = list(entity_dict.keys())
        frequencies = list(entity_dict.values())
        squarify.plot(sizes=frequencies, label=labels, color=color_palette("Spectral", len(labels)), alpha=0.7, pad=2)

        plt.title(title, fontweight = "bold")
        plt.savefig(destination)
        plt.close()
        logger.info(f"Treemap created in {destination}")

    except Exception as e:
        logger.exception(f"Treemap failed: {e} in {destination}")

def main():
    try:
        input_folder_name, output_folder_name = FOLDER_NAMES['input_folder_name'], FOLDER_NAMES['output_folder_name']
        input_file_name = 'P0DTC2.xml'
        output_json_name = 'virus.json'
        output_graph_name = 'treemap.png'

        source = get_join_path(input_folder_name, input_file_name, is_sample=True)
        destination_json = get_join_path(output_folder_name, output_json_name, is_sample=True)
        destination_graph = get_join_path(output_folder_name, output_graph_name, is_sample=True)

        virus_descriptions = get_dict_xml(source=source, events=('start', 'end'),
                                          tags = ('accession', 'comment'), attributes=(None, ('type', 'function')))
        write_json(destination_json, virus_descriptions)
        entity_dict = get_entity_dict(virus_descriptions, nlp)
        get_treemap(destination_graph, entity_dict, title='Distribution of Entity Labels')
        logger.info(f"Successfully executed: {basename(__file__)}")

    except Exception as e:
        logger.exception(f"Error in main function: {e} in {basename(__file__)}")

if __name__ == '__main__':
    main()
