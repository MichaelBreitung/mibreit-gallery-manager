import argparse
import os
import xml.etree.ElementTree as XmlEt
from PIL import Image

# global constants
REQUIRED_GALLERY_FOLDER_IMAGES = "images"
REQUIRED_GALLERY_FOLDER_SMALL = "small"
REQUIRED_GALLERY_FILE_GALLERY = "gallery.xml"
REQUIRED_GALLERY_ELEMENTS =  {REQUIRED_GALLERY_FILE_GALLERY,
                             REQUIRED_GALLERY_FOLDER_IMAGES, REQUIRED_GALLERY_FOLDER_SMALL}
SUPPORTED_IMAGE_FORMATS = (".jpg", ".jpeg")
THUMBNAIL_SIZE = (200,200)
GALLERY_XML_IMAGES_TAG = "images"
GALLERY_XML_IMAGES_FILENAMW_TAG = "filename"

# Function definitions
def get_absolute_path(input):
    gallery_path = os.path.normcase(input)

    if not os.path.isdir(gallery_path):
        gallery_path = os.path.normpath(
            os.path.join(os.getcwd(), gallery_path))

    if not os.path.isdir(gallery_path):
        raise ValueError(f"Invalid Input: {input}")

    return gallery_path

def is_gallery_path(path):
    return REQUIRED_GALLERY_ELEMENTS <= set(os.listdir(path))

def get_list_of_supported_images_from_path(path):
    files = os.listdir(path)
    return [file for file in files if file.endswith(SUPPORTED_IMAGE_FORMATS)]

def extract_filename_from_image_element(element: XmlEt.ElementTree):
        return element.find(GALLERY_XML_IMAGES_FILENAMW_TAG).text

def get_list_of_images_from_gallery(xml_gallery_tree):     
    xmlImages = map(extract_filename_from_image_element ,xml_gallery_tree.getroot().find(GALLERY_XML_IMAGES_TAG))
    return xmlImages

def create_missing_thumbs(missing_thumbs_list, abs_gallery_path):
    images_path = os.path.join(abs_gallery_path, REQUIRED_GALLERY_FOLDER_IMAGES)
    thumbs_path = os.path.join(abs_gallery_path, REQUIRED_GALLERY_FOLDER_SMALL)
    for thumb_name in missing_thumbs_list:
        print(f"create_missing_thumbs: creating missing thumb -> {thumb_name}")
        thumb = Image.open(os.path.join(images_path, thumb_name)).copy()
        thumb.thumbnail(THUMBNAIL_SIZE)
        thumb.save(os.path.join(thumbs_path, thumb_name))

def remove_superfluous_thumbs(superfluous_thumbs_list, abs_gallery_path):
    thumbs_path = os.path.join(abs_gallery_path, REQUIRED_GALLERY_FOLDER_SMALL)
    for thumb_name in superfluous_thumbs_list:
        print(f"remove_superfluous_thumbs: removing superfluous thumb -> {thumb_name}")
        os.remove(os.path.join(thumbs_path, thumb_name))

def synchronize_gallery_elements(missing_gallery_elements, superfluous_gallery_elements, images_path, xml_gallery_tree):
    images_element = xml_gallery_tree.getroot().find(GALLERY_XML_IMAGES_TAG)
    # check for images to remove from gallery
    for image_element in images_element:
        image_name = extract_filename_from_image_element(image_element)
        if image_name in superfluous_gallery_elements:
            print(f"synchronize_gallery_elements: element to synchronize -> {image_name}")
            # means it's not present in images folder
            # Inform user and ask if it shall be removed
            response = input(f"The image {image_name} is present in {REQUIRED_GALLERY_FILE_GALLERY}, but not in {REQUIRED_GALLERY_FOLDER_IMAGES}. Shall it be removed from {REQUIRED_GALLERY_FILE_GALLERY}? (yes/no) ")
            if response == "yes":
                images_element.remove(image_element)
    # check for images to remove from images folder
    for image_name in missing_gallery_elements:
        print(f"synchronize_gallery_elements: element to synchronize -> {image_name}")
        response = input(f"The image {image_name} is present in {REQUIRED_GALLERY_FOLDER_IMAGES}, but not in {REQUIRED_GALLERY_FILE_GALLERY}. Shall it be removed from {REQUIRED_GALLERY_FOLDER_IMAGES}? (yes/no) ")
        if response == "yes":
            os.remove(os.path.join(images_path, image_name))
        else:
            response = input(f"Shall it instead be created inside {REQUIRED_GALLERY_FILE_GALLERY}? (yes/no) ")  

# Start of Main Program
parser = argparse.ArgumentParser("mibreit-gallery-manager")
parser.add_argument("-i", "--input", required=True, type=str,
                    help="The folder in which the galleries are located. Recursion will be used to find all individual galleries.")

cmd_args = parser.parse_args()
abs_path = get_absolute_path(cmd_args.input)

if is_gallery_path(abs_path):
    # 1) get different image sets for synchronization
    images_set = set(get_list_of_supported_images_from_path(os.path.join(abs_path, REQUIRED_GALLERY_FOLDER_IMAGES)))
    thumbs_set = set(get_list_of_supported_images_from_path(os.path.join(abs_path, REQUIRED_GALLERY_FOLDER_SMALL)))
    xml_gallery_tree = XmlEt.parse(os.path.join(abs_path, REQUIRED_GALLERY_FILE_GALLERY))
    images_in_gallery_set = set(get_list_of_images_from_gallery(xml_gallery_tree))
    
    # 2) synchronize gallery set with images set
    missing_gallery_elements = images_set - images_in_gallery_set
    superfluous_gallery_elements = images_in_gallery_set - images_set
    synchronize_gallery_elements(missing_gallery_elements, superfluous_gallery_elements, os.path.join(abs_path, REQUIRED_GALLERY_FOLDER_IMAGES), xml_gallery_tree)
    xml_gallery_tree.write(os.path.join(abs_path, REQUIRED_GALLERY_FILE_GALLERY))

    # 3) update images set
    images_set = set(get_list_of_supported_images_from_path(os.path.join(abs_path, REQUIRED_GALLERY_FOLDER_IMAGES)))

    # 4) synchronize thumbs set with images set
    missing_thumbs_set = images_set - thumbs_set
    superfluous_thumbs_set = thumbs_set - images_set

    if len(missing_thumbs_set):
        print(f"Thumbs are missing in gallery ({abs_path}). Missing thumbs: {missing_thumbs_set}")
        create_missing_thumbs(missing_thumbs_set, abs_path)

    if len(superfluous_thumbs_set):
        print(f"Superfluous Thumbs in gallery ({abs_path}). Superfluous thumbs: {superfluous_thumbs_set}")
        remove_superfluous_thumbs(superfluous_thumbs_set, abs_path)


