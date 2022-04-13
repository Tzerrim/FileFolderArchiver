import argparse
import logging
import os

# initial variables from arguments
total = 0
start_directory_number = 0
quantity = 0
source_dir = ""
destination_dir = ""
log_file = ""
verbose = False
# global variables for selfcheck and statistics
processed_quantity = 0
folders_created = {}
log_dateformat = '%d-%b-%y %H:%M:%S'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt=log_dateformat)


def log(string):
    if verbose:
        logging.info(string)


def get_subdirectories(path):
    directory_contents = os.listdir(path)
    directories = []
    for item in directory_contents:
        if os.path.isdir(path + item):
            directories.append(item)
    return directories


def prepare_directory_dict(path, number_of_files):
    directories_and_number_of_files = {}
    subdirectories = get_subdirectories(path)
    directory_number = start_directory_number
    while number_of_files > 0:
        files_in_folder_quantity = get_files_quantity_in_folder(path + str(directory_number))
        if str(directory_number) not in subdirectories or quantity > files_in_folder_quantity:
            number_of_files_to_move = quantity - files_in_folder_quantity
            directories_and_number_of_files[directory_number] = number_of_files_to_move
            number_of_files = number_of_files - number_of_files_to_move
        directory_number += 1
    return directories_and_number_of_files


def move_file(source_path, destination_path, files):
    if not os.path.isdir(destination_path):
        os.mkdir(destination_path)
        folders_created[destination_path] = files
        log("Creating folder: " + destination_path)
    for index, item in enumerate(files):
        log("Moving file. Index: " + str(index) + "\t" + source_path + item + " -> " + destination_path + item)
        os.rename(source_path + item, destination_path + item)


def get_files_list(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def get_files_quantity_in_folder(path):
    if os.path.exists(path) and os.path.isdir(path):
        return len(os.listdir(path))
    return 0


def execute_script():
    files_to_move = get_files_list(source_dir)
    total = len(files_to_move)
    log("Number of files to move: " + str(total))
    files_directory_dict = prepare_directory_dict(destination_dir, len(files_to_move))
    for directory in files_directory_dict:
        quantity_files_to_move = files_directory_dict[directory]
        move_file(source_dir, destination_dir + str(directory) + "/", files_to_move[0: quantity_files_to_move])
        del files_to_move[0: quantity_files_to_move]
    logging.info("Done")


def validate_path(path):
    if os.path.exists(path) and os.access(os.path.dirname(path), os.W_OK):
        return True
    else:
        return False


# processing incoming arguments: path, file quantity, verbosity flag
parser = argparse.ArgumentParser()

parser.add_argument('-s', action="store", dest="source_dir", default="", required=True, help="Source directory path")
parser.add_argument('-q', action="store", dest="quantity", default="100", type=int, required=True,
                    help="Number of files in folder")
parser.add_argument('-v', action="store_true", dest="verbose", help="More verbose output")
parser.add_argument('-l', action="store", dest="log_file_name", default="", help="Log file name. Format: NAME.log")
parser.add_argument('-n', action="store", dest="start_directory_number", default="0", type=int,
                    help="Folder number from what count starts")
parser.add_argument('-d', action="store", dest="destination_dir", default="",
                    help="Destination directory path")

args = parser.parse_args()

source_dir = args.source_dir
destination_dir = args.destination_dir
quantity = args.quantity
verbose = args.verbose
log_file = args.log_file_name
start_directory_number = args.start_directory_number

try:

    if log_file:  # and regex.match(log_file)
        logger = logging.getLogger()
        handler = logging.FileHandler(destination_dir+log_file)
        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', datefmt=log_dateformat)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logging.info("Source directory: " + str(source_dir))
    logging.info("Destination directory: " + str(destination_dir if destination_dir else "NOT SET"))
    logging.info("Files quantity per directory: " + str(quantity))
    logging.info("Log file: " + str(log_file if log_file else "NOT SET"))
    logging.info("Verbose mode: " + str("TRUE" if verbose else "FALSE"))
    logging.info("Directory start count: " + str(start_directory_number if start_directory_number else "NOT SET"))

    if not destination_dir:
        logging.warning("Destination directory is not set. Source directory will be used as destination directory")
        destination_dir = source_dir

    execute_script()

    total = 0
    for x in folders_created:
        total += len(folders_created[x])
        logging.info("Folder: " + str(x) + " : " + str(len(folders_created[x])))
    logging.info("Total: " + str(total))

except FileNotFoundError:
    logging.error("No such file or directory")
    logging.exception("message")
except:
    logging.error("Unexpected exception")
    logging.exception("message")

# call example  python3 ./main.py -s ~/Images/Source_Folder/ -q 14 -v -l log1.log -d ~/Images/Destination_Folder/
