import argparse
import os
import logging

# import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# initial variables from arguments
start_directory_number = 0
quantity = 0
source_dir = ""
destination_dir = ""
log_file = ""
verbose = False
# global variables for selfcheck and statistics
processed_quantity = 0
folders_created = {}


# Constants


# REGEX_LOGFILE = "[^\\]*\.(\w+)$"


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


def get_first_folder_index(path):
    subdirectories = get_subdirectories(path)
    for i in range(start_directory_number, start_directory_number + len(subdirectories) + 1):
        if str(i) in subdirectories:
            continue
        else:
            return i
    return start_directory_number


def get_files_list(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def check_files_number_in_folder(path):
    return len(os.listdir(path))


def execute_script(path, number):
    files_to_move = get_files_list(path)
    log("Number of files to move: " + str(len(files_to_move)))
    while len(files_to_move) > 0:
        folder_index = get_first_folder_index(path)

        # if folder does not exist
        if not os.path.isdir(path + "/" + str(folder_index)):
            os.mkdir(path + "/" + str(folder_index))
            log("Creating folder: " + path + "/" + str(folder_index))

        files_to_move = get_files_list(path)
        files_in_destination = get_files_list(os.path.join(path, str(folder_index)))
        number_of_files_to_move_in_folder = number - len(files_in_destination)

        folders_created[folder_index] = []

        # if in folder already have more files than we move per iteration
        if number_of_files_to_move_in_folder < 0:
            folder_index += 1
            os.mkdir(path + str(folder_index))
            number_of_files_to_move_in_folder = number
            logging.info("Creating folder: ", path + str(folder_index))

        if len(files_to_move) < number_of_files_to_move_in_folder:
            number_of_files_to_move_in_folder = len(files_to_move)

        log("Number of files rest: " + str(len(files_to_move)))
        log("Number of files to move : " + str(number_of_files_to_move_in_folder))

        iteration_files = files_to_move[0: number_of_files_to_move_in_folder]

        for index, item in enumerate(iteration_files):
            log("Moving file. Index: " + str(index) + "\t" + path + item + " -> " + path + str(
                folder_index) + "/" + item)
            os.rename(path + item, path + str(folder_index) + "/" + item)
            folders_created[folder_index].append(item)

        del files_to_move[0: number_of_files_to_move_in_folder]

    logging.info("Done")


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
                    help="Destination directory path")  # TODO make settable a destination folder

args = parser.parse_args()

source_dir = args.source_dir
destination_dir = args.destination_dir
quantity = args.quantity
verbose = args.verbose
log_file = args.log_file_name
start_directory_number = args.start_directory_number

# regex = re.compile(REGEX_LOGFILE)

try:

    if log_file:  # and regex.match(log_file)
        logger = logging.getLogger()
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logging.info("Source directory: " + str(source_dir))
    logging.info("Destination directory: " + str(destination_dir if destination_dir else "NOT SETTED"))
    logging.info("Files quantity pre directory" + str(quantity))
    logging.info("Log file: " + str(log_file if log_file else "NOT SET"))
    logging.info("Verbose mode: " + str("TRUE" if verbose else "FALSE"))
    logging.info("Directory start count: " + str(start_directory_number if start_directory_number else "NOT SET"))

    if quantity > 0 and source_dir != "":
        execute_script(source_dir, quantity)
    else:
        logging.error("Wrong arguments. -s - directory, -q - file quantity")

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

# call example  python ./main.py -s ~/Img/Test/Not_Sorted/ -q 14 -v
