import argparse
import os
from gallery_synchronizer import GallerySynchronizer, is_gallery_path

# Function definitions
def get_absolute_path(input):
    gallery_path = os.path.normcase(input)

    if not os.path.isdir(gallery_path):
        gallery_path = os.path.normpath(
            os.path.join(os.getcwd(), gallery_path))

    if not os.path.isdir(gallery_path):
        raise ValueError(f"Invalid Input: {input}")

    return gallery_path

# Start of Main Program
parser = argparse.ArgumentParser("mibreit-gallery-manager")
parser.add_argument("-i", "--input", required=True, type=str,
                    help="The folder in which the galleries are located. Recursion will be used to find all individual galleries.")

cmd_args = parser.parse_args()
abs_path = get_absolute_path(cmd_args.input)

if is_gallery_path(abs_path):
   gallery_sync = GallerySynchronizer(abs_path)
   gallery_sync.synchronize()


