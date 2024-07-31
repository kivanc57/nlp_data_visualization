import logging
"""
This is the initialization file for the 'src' package.
"""

# Import specific functions or classes to make them available at the package level
from src.freq_barplot import get_list_xml, write_txt, get_frequency_list, get_bar_plot
from src.len_histogram import get_doc, get_sentence_lengths, get_histogram
from src.sentiment_piechart import get_texts, get_sentiments, categorize_sentiments, get_pie_chart
from src.entity_treemap import get_dict_xml, write_json, get_entity_dict, get_treemap
from src.len_violin_plot import get_mails, write_excel, get_length_list, get_violin_plot
from src.pos_cloud import get_sgms, get_docs, detect_pos, write_csv, get_word_cloud
from config.common_config import basename, configure_logging
from config.constants import FOLDER_NAMES

#Configure logging
script_name = basename(__file__)[:-3]
configure_logging(script_name)
logger = logging.getLogger(__name__)
logger.info("Package is initialized")

#Metadata
__version__ = "1.0.0"
__date__ = "31-07-2024"
__email__ = "kivancgordu@hotmail.com"
__status__ = "production"

__all__ = [
    'get_list_xml', 'write_txt', 'get_frequency_list', 'get_bar_plot',
    'get_doc', 'get_sentence_lengths', 'get_histogram',
    'get_texts', 'get_sentiments', 'categorize_sentiments', 'get_pie_chart',
    'get_dict_xml', 'write_json', 'get_entity_dict', 'get_treemap',
    'get_mails', 'write_excel', 'get_length_list', 'get_violin_plot',
    'get_sgms', 'get_docs', 'detect_pos', 'write_csv', 'get_word_cloud', 'FOLDER_NAMES'
]
