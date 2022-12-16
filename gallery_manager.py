import argparse
import os
from modules.gallery_synchronizer import synchronize_gallery
from modules.gallery_tools import is_gallery_path


def get_valid_path(input):
    gallery_path = os.path.normcase(input)

    if not os.path.isdir(gallery_path):
        gallery_path = os.path.normpath(
            os.path.join(os.getcwd(), gallery_path))

    if not os.path.isdir(gallery_path):
        raise ValueError(f"Invalid Input: {input}")

    return gallery_path


def synchronize_galleries_in_folder(folder):
    if is_gallery_path(folder):
        synchronize_gallery(folder)
    else:
        for it in os.scandir(folder):
            if it.is_dir():
                synchronize_galleries_in_folder(it.path)


# Start of Main Program
parser = argparse.ArgumentParser("mibreit-gallery-manager")
parser.add_argument("-i", "--input", required=True, type=str,
                    help="The folder in which the galleries are located. Recursion will be used to find all individual galleries.")

cmd_args = parser.parse_args()
path = get_valid_path(cmd_args.input)

synchronize_galleries_in_folder(path)
