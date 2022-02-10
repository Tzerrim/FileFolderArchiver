import argparse
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# initial variables from arguments
source_dir = ""
quantity = 0
verbose = False
# global variables for selfcheck and statistics
processed_quantity = 0
folders_created = {}
# Constants
DEFAULT_FIRST_DIRECTORY_NAME = 0


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
    for i in range(0, len(subdirectories) + 1):
        if str(i) in subdirectories:
            continue
        else:
            return i
    return DEFAULT_FIRST_DIRECTORY_NAME


def get_files_list(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def check_files_number_in_folder(path):
    return len(os.listdir(path))


def execute_script(path, number):
    files_to_move = get_files_list(path)
    while len(files_to_move) > 0:
        folder_index = get_first_folder_index(path)

        # if folder does not exist
        if not os.path.isdir(path + "/" + str(folder_index)):
            os.mkdir(path + "/" + str(folder_index))

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

        logging.info("Number of files rest: ", len(files_to_move))
        logging.info("Number of files to move : ", number_of_files_to_move_in_folder)

        iteration_files = files_to_move[0: number_of_files_to_move_in_folder]

        for index, item in enumerate(iteration_files):
            logging.info("Moving file. Index: ", index, "From path: ", path + item, "To path: ",
                         path + str(folder_index) + "/" + item)
            os.rename(path + item, path + str(folder_index) + "/" + item)
            folders_created[folder_index].append(item)

        del files_to_move[0: number_of_files_to_move_in_folder]

    logging.info("Done")


# processing incoming arguments: path, file quantity, verbosity flag
parser = argparse.ArgumentParser()

parser.add_argument('-s', action="store", dest="source_dir", default="", help="Source dir")
parser.add_argument('-q', action="store", dest="quantity", default="0", type=int, help="Number of files in folder")
parser.add_argument('-v', action="store_true", dest="verbose", help="More verbose output")

args = parser.parse_args()

source_dir = args.source_dir
quantity = args.quantity
verbose = args.verbose


try:
    if quantity > 0 and source_dir != "":
        execute_script(source_dir, quantity)
    else:
        logging.error("Wrong arguments. -s - directory, -q - file quantity")

    total = 0
    for x in folders_created:
        total += len(folders_created[x])
        logging.info(str(x) + " : " + str(len(folders_created[x])))
    logging.info("Total: " + str(total))

    print(folders_created)

except FileNotFoundError:
    logging.error("No such file or directory")
# call example  python ./main.py -s ~/Img/Test/Not_Sorted/ -q 14 -v
