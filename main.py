import argparse
import os

# Initialize variables
source_dir = ""
quantity = 0
# Constants
DEFAULT_FIRST_DIRECTORY_NAME = 0


def get_subdirectories(path):
    directory_contents = os.listdir(path)
    directories = []
    for item in directory_contents:
        if os.path.isdir(path+item):
            directories.append(item)
    return directories


def get_first_folder_index(path):
    subdirectories = get_subdirectories(path)
    for i in range (0, len(subdirectories)+1):
        if str(i) in subdirectories:
           continue
        else:
            return i
    return DEFAULT_FIRST_DIRECTORY_NAME


def get_files_list(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def check_files_number_in_folder(path):
    return len(os.listdir(path))


def execute_script (path, number):
    files_to_move = get_files_list(path)
    while len(files_to_move) > 0:
        folder_index = get_first_folder_index(path)

        # if folder does not exist
        if not os.path.isdir(path+"/"+str (folder_index)):
            os.mkdir(path + "/" + str (folder_index))

        files_to_move = get_files_list(path)
        files_in_destiantion = get_files_list(os.path.join(path, str (folder_index)))
        number_of_files_to_move_in_folder = number - len(files_in_destiantion)

        # if in folder already are more files than we move per iteration
        if number_of_files_to_move_in_folder < 0:
            folder_index+=1
            os.mkdir(path + str (folder_index))
            number_of_files_to_move_in_folder = number
            print("Creating folder: ", path + str (folder_index))

        # Moving
        for i in range(0, number_of_files_to_move_in_folder):
            print("Moving file: ", path+files_to_move[i])
            os.rename(path+files_to_move[i], path+str (folder_index)+"/"+files_to_move[i])
            print("End filling folder: ", path + str (folder_index)+"/")
            files_to_move.pop(i)
    print("Done")

# Processing incoming arguments: path and file quantity
parser = argparse.ArgumentParser()

parser.add_argument('-s', action="store", dest="source_dir", default="", help="Source dir")
parser.add_argument('-q', action="store", dest="quantity", default="0", type=int, help="Number of files in folder")

args = parser.parse_args()

source_dir = args.source_dir
quantity = args.quantity

if quantity > 0 and source_dir != "":
    execute_script(source_dir, quantity)
else:
    print("Wrong arguments. -d - directory, -q - file quantity")