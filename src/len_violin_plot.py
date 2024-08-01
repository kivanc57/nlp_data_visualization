import re
from pandas import DataFrame
import logging
import matplotlib.pyplot as plt
from seaborn import violinplot


#Load configs
from config.common_config import get_join_path, basename, configure_logging
from config.constants import FOLDER_NAMES

#Configure logging
script_name = basename(__file__)[:-3]
configure_logging(script_name)
logger = logging.getLogger(__name__)


def get_mails(source):
    mails = list()

    try:
        with open(source, mode='r', encoding='utf-8', errors='replace') as f:
            for line in f:
                found_mails = re.findall("\w+@\w+\.\w+", line)
                mails.extend(found_mails)
        logger.info(f"Extraction succeeded: {source}")
        return mails

    except Exception as e:
        logger.exception(f"Failed extracting: {e} in {source}")
        return None

def write_excel(destination, data, columns=['Mails']):
    try:
        df = DataFrame(data, columns=columns)
        df.to_excel(destination, index=True, sheet_name='Sheet_1')
        logger.info(f"Writing succeeded: {destination}")

    except Exception as e:
        logger.exception(f"Failed writing: {e} in {destination}")
        return None
    
def get_length_list(mails):
    try:
        length_list =  [len(mail) for mail in mails]
        logger.info("Created length list")
        return length_list
    
    except Exception as e:
        logger.exception(f"Failed length list: {e}")
        return None

def get_violin_plot(destination, data, column_name, title=None, color='Yellow'):
    try:
        data_df = DataFrame(data=data, columns=[column_name])
        plt.figure(figsize=(10, 6))
        violinplot(x=column_name, data=data_df, color=color)
        plt.xlabel(column_name)
        plt.title(title, fontweight = "bold")
        plt.savefig(destination)
        logger.info(f"Graph created in {destination}")

    except Exception as e:
        logger.exception(f"Graph failed: {e} in {destination}")

def main():
    try:
        input_folder_name, output_folder_name = FOLDER_NAMES['input_folder_name'], FOLDER_NAMES['output_folder_name']
        input_txt_name = 'emails_short.txt'
        output_graph_name = 'violin_plot.png'
        output_file_name = 'found_mails.xlsx'

        source = get_join_path(input_folder_name, input_txt_name, is_sample=True)
        destination_txt = get_join_path(output_folder_name, output_file_name, is_sample=True)
        destination_graph = get_join_path(output_folder_name, output_graph_name, is_sample=True)

        mail_list = get_mails(source)
        write_excel(destination_txt, mail_list, columns=['Mails'])
        length_list = get_length_list(mail_list)
        get_violin_plot(destination_graph, length_list, column_name='Length', title='Length Distribution of Texts', color='Yellow')

        logger.info(f"Successfully executed: {basename(__file__)}.")

    except Exception as e:
        logger.exception(f"Error occurred in main function: {e}")

if __name__ == '__main__':
    main()
