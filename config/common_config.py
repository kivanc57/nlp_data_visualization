import logging
from os.path import dirname, abspath, join, basename
from os import makedirs

#Create separate log for each file with its name 
def get_log_path(script_name, log_folder='logs'):
    project_path = dirname(dirname(abspath(__file__)))
    log_folder_path = join(project_path, log_folder)
    makedirs(log_folder_path, exist_ok=True) #Create the folder if does not exist
    log_file_name = f"{script_name}.log"
    full_path = join(log_folder_path, log_file_name)
    return full_path

#Configures logging in each script
def configure_logging(script_name):
        log_file = get_log_path(script_name)
        logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='a'),
            logging.StreamHandler()
        ],
    )

#Adjust this os function in each function to find inpput and output paths
def get_join_path(folder_name, file_name, is_sample=False):
    try:
        project_path = dirname(dirname(abspath(__file__)))
        if is_sample:
            folder_path = join('data', folder_name, 'sample')
        else:
            folder_path = join('data', folder_name)
        full_path = join(project_path, folder_path, file_name)
        return full_path
    
    except Exception as e:
        print(f"Error: {e} joining {folder_name} and {file_name}")
