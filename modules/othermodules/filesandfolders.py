import os
import sys

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
