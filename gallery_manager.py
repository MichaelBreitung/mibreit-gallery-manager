"""Module used to parse command line arguments"""
import argparse
import os
from modules.gallery_tools import is_gallery_path, get_valid_path, get_images_path, get_thumbs_path
from modules.gallery_exif_tool import GalleryExifUpdate, read_configuration
from modules.gallery_xml_tools import parse_gallery_xml, update_image_descriptions, get_images_element, \
    write_formatted_xml, read_gallery_xml, update_gallery_description, get_info_element
from modules.gallery_xml_updater import *
from modules.gallery_thumb_updater import *


def synchronize_gallery(folder: str):
    print("\nSynchronizing gallery -> ", folder)
    images_path = get_images_path(folder)
    thumbs_path = get_thumbs_path(folder)

    if GalleryXmlUpdater(images_path, folder).update() is True:
        GalleryThumbUpdater(images_path, thumbs_path).update()
    else:
        print(
            f"Invalid Gallery under {path}. The {REQUIRED_GALLERY_FILE_GALLERY} is invalid.")


def synchronize_galleries_in_folder(folder: str) -> None:
    if is_gallery_path(folder):
        synchronize_gallery(folder)
    else:
        for folder_element in os.scandir(folder):
            if folder_element.is_dir():
                synchronize_galleries_in_folder(folder_element.path)


def update_image_descriptions_in_folder(folder: str, exif_updater: GalleryExifUpdate) -> None:
    if is_gallery_path(folder):
        print("\nUpdating image descriptions in gallery -> ", folder)
        xml_data = read_gallery_xml(folder)
        xml_gallery_tree = parse_gallery_xml(xml_data)
        if xml_gallery_tree is not None:
            info_en_element = get_info_element(xml_gallery_tree)
            info_de_element = get_info_element(xml_gallery_tree, True)
          
            update_gallery_description(info_en_element, info_de_element)

            images_element = get_images_element(xml_gallery_tree)

            def update_image_callback(image_name, image_title, image_description):
                images_path = get_images_path(folder)
                exif_updater.update(
                    images_path, image_name, image_title, image_description)

            update_image_descriptions(images_element, update_image_callback)

            write_formatted_xml(xml_gallery_tree, folder)
        else:
            print(f"Exception: parsing of {REQUIRED_GALLERY_FILE_GALLERY} failed for \
                {folder}")
    else:
        for folder_element in os.scandir(folder):
            if folder_element.is_dir():
                update_image_descriptions_in_folder(folder_element.path, exif_updater)


# Start of Main Program
parser = argparse.ArgumentParser("mibreit-gallery-manager")
parser.add_argument("-i", "--input", required=True, type=str,
                    help="The folder in which the galleries are located. \
                        Recursion will be used to find all individual galleries.")
parser.add_argument("-d", "--description", default=False,
                    action=argparse.BooleanOptionalAction,
                    help="Add this flag, to update the descriptions of the photos \
                        within the input galleries.")
parser.add_argument("-c", "--config", type=str,
                    required=False, help="Path to config file (json)")


cmd_args = parser.parse_args()
config = None

if cmd_args.config:
    config = read_configuration(cmd_args.config)

gallery_exif_update = GalleryExifUpdate(config)

path: str = get_valid_path(cmd_args.input) # type: ignore

if cmd_args.description:
    update_image_descriptions_in_folder(path, gallery_exif_update) # type: ignore
else:
    synchronize_galleries_in_folder(path) # type: ignore
