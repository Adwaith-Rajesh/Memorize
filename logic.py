import os
from typing import List
from random import shuffle


def get_file_names_of_pics(folder: str,
                           avoid: List[str] = [],
                           extn: str = "") -> List[str]:
    """
    Get all the PNG file from a directory
    :param folder: the path to the folder to look for files
    :param avoid: the names of the files to be avoided
    :param extn: The extension of the image file
    """
    file_names = [name for name in os.listdir(folder) if name not in avoid]
    if extn:
        file_names = [name for name in file_names if name.endswith(extn)]
    return file_names


def get_my_name(names: List[str]) -> str:
    shuffle(names)
    return names.pop() if names else ""