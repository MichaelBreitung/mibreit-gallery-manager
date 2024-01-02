"""Module used to parse command line arguments"""
import argparse
import os
from modules.gallery_tools import is_gallery_path, get_valid_path, get_images_path, get_thumbs_path, get_medium_path
from modules.gallery_exif_tool import GalleryExifUpdate, read_configuration
from modules.gallery_xml_tools import parse_gallery_xml, update_image_descriptions, get_images_element, \
    write_formatted_xml, read_gallery_xml, update_gallery_description, get_info_element
from modules.gallery_xml_updater import GalleryXmlUpdater, GALLERY_FILE_GALLERY
from modules.gallery_variants_updater import *
from modules.gallery_create import GalleryCreator


def synchronize_gallery(folder: str, exif_updater: GalleryExifUpdate):
    print("\nSynchronizing gallery -> ", folder)
    images_path = get_images_path(folder)
    thumbs_path = get_thumbs_path(folder)
    medium_path = get_medium_path(folder)

    def update_image_callback(image_name, image_title, image_description):
        exif_updater.update(
            images_path, image_name, image_title, image_description)

    if GalleryXmlUpdater(images_path, folder, update_image_callback).update() is True:
        GalleryVariantsUpdater(images_path, thumbs_path).update()
        GalleryVariantsUpdater(images_path, medium_path, False).update()
    else:
        print(
            f"Invalid Gallery under {path}. The {GALLERY_FILE_GALLERY} is invalid.")


def synchronize_galleries_in_folder(folder: str, exif_updater: GalleryExifUpdate) -> None:
    if is_gallery_path(folder):
        synchronize_gallery(folder, exif_updater)
    else:
        for folder_element in os.scandir(folder):
            if folder_element.is_dir():
                synchronize_galleries_in_folder(folder_element.path, exif_updater)


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
            print(f"Exception: parsing of {GALLERY_FILE_GALLERY} failed for \
                {folder}")
    else:
        for folder_element in os.scandir(folder):
            if folder_element.is_dir():
                update_image_descriptions_in_folder(folder_element.path, exif_updater)

def create_new_gallery_in_folder(folder: str) -> None:
    print("\nCreating new gallery in ", folder)
    GalleryCreator(folder).create()

# Start of Main Program
parser = argparse.ArgumentParser("mibreit-gallery-manager")
parser.add_argument("-i", "--input", required=True, type=str,
                    help="The folder in which the galleries are located. \
                        Recursion will be used to find all individual galleries.")
parser.add_argument("-d", "--description", default=False,
                    action=argparse.BooleanOptionalAction,
                    help="Add this flag, to update the descriptions of the photos \
                        within the input galleries.")
parser.add_argument("-n", "--new", default=False,
                    action=argparse.BooleanOptionalAction,
                    help="Add this flag, to create a new, empty gallery within the input \
                        galleries folder.")
parser.add_argument("-c", "--config", type=str,
                    required=False, help="Path to config file (json)")


cmd_args = parser.parse_args()
config = None

if cmd_args.config:
    config = read_configuration(cmd_args.config)

gallery_exif_update = GalleryExifUpdate(config)

path: str = get_valid_path(cmd_args.input) # type: ignore

if cmd_args.new:
    create_new_gallery_in_folder(path) # type: ignore
elif cmd_args.description:
    update_image_descriptions_in_folder(path, gallery_exif_update) # type: ignore
else:
    synchronize_galleries_in_folder(path, gallery_exif_update) # type: ignore
