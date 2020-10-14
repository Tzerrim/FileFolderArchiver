import argparse
import os

# Initialize varibles
source_dir = ""
quantity = 0
# Constants
DEFAULT_FIRST_DIRECTORY_NAME = "0"


def get_subdirectories(path):
    directory_contents = os.listdir(path)
    directories = []
    for item in directory_contents:
        if os.path.isdir(item):
            directories.append(item)
    return directories


def get_first_folder_index(path):
    subdirectories = get_subdirectories(path)
    for i in range (0, len(subdirectories)):
        if i in subdirectories:
            i += 1
            return str(i)
    return DEFAULT_FIRST_DIRECTORY_NAME


def get_files_to_move_list (path, directory_name):
    pass

def get_files_list(path):
    return [f for f in os.listdir(path) if os.isfile(os.join(path, f))]


def check_files_number_in_folder(path):
    return len(os.listdir(path))


def execute_script (path):
    folder_index = get_first_folder_index(path)

    # if folder does not exist
    if not os.path.isdir(path+"/"+folder_index):
        os.mkdir(path + "/" + folder_index)

    files_to_move = get_files_list(path)
    files_in_destiantion = get_files_list(os.join(path, folder_index))
    number_of_files_to_move_in_folder = quantity - len(files_in_destiantion)

    # if in folder already are more files than we move per iteration
    if number_of_files_to_move_in_folder <= 0:
        folder_index+=1
        os.mkdir(path + "/" + folder_index)


# Processing incoming arguments: path and file quantity
parser = argparse.ArgumentParser()

parser.add_argument('-s', action="store", dest="source_dir", default="", help="Source dir")
parser.add_argument('-q', action="store", dest="quantity", default="0", type=int, help="Number of files in folder")

args = parser.parse_args()

source_dir = args.source_dir
quantity = args.quantity

if quantity > 0 and source_dir != "":
    execute_script()
else:
    print("Wrong arguments. -d - directory, -q - file quantity")