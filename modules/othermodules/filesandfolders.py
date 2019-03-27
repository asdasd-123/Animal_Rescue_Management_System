import os
import sys
from shutil import copy2

# print(sys.path[0]) (get path of current script)


def check_folder(folder_path, create=False):
    if not os.path.exists(folder_path):
        if create:
            os.makedirs(folder_path)
        return False
    return True


def check_rel_folder(relative_path, create=False):
    full_path = os.path.join(sys.path[0], relative_path)
    if not os.path.exists(full_path):
        if create:
            os.makedirs(full_path)
        return False
    return True


def get_full_path(relative_path):
    return os.path.join(sys.path[0], relative_path)


def check_rel_file(relative_path):
    full_path = os.path.join(sys.path[0], relative_path)
    if os.path.isfile(full_path):
        return True
    else:
        return False


def file_extension(path):
    return os.path.splitext(path)[1]


def copy_files(source_path, dest_path):
    copy2(source_path, dest_path)


def open_folder(path):
    os.startfile(path)


def get_rel_file_list(folder_path, return_type='files'):
    """
    Accepts a relative folder path
    return_type = files     - List of files
    return_type = paths     - List of path+file names
    """
    full_path = os.path.join(sys.path[0], folder_path)
    results = os.listdir(full_path)
    if return_type == 'paths':
        for index, item in enumerate(results):
            results[index] = os.path.join(folder_path, item)
    return results


def get_file_list(full_folder_path, return_type='files'):
    """
    Accepts a full folder path
    return_type = files     - List of files
    return_type = paths     - List of path+file names
    """
    results = os.listdir(full_folder_path)
    if return_type == 'paths':
        for index, item in enumerate(results):
            results[index] = os.path.join(full_folder_path, item)
    return results
