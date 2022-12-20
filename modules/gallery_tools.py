from os import listdir
import xml.etree.ElementTree as XmlEt
from .gallery_configuration import REQUIRED_GALLERY_ELEMENTS, GALLERY_XML_IMAGES_TAG, REQUIRED_GALLERY_FILE_GALLERY

SUPPORTED_IMAGE_FORMATS = (".jpg", ".jpeg")


def get_list_of_supported_images_in_folder(folder):
    files = listdir(folder)
    return [file for file in files if file.endswith(SUPPORTED_IMAGE_FORMATS)]


def is_gallery_path(path):
    return REQUIRED_GALLERY_ELEMENTS <= set(listdir(path))


def parse_gallery_xml(gallery_xml_path):
    try:
        xml_gallery_tree = XmlEt.parse(gallery_xml_path)
        if xml_gallery_tree.getroot().find(GALLERY_XML_IMAGES_TAG) is None:
            return None
        return xml_gallery_tree
    except Exception as inst:
        print(
            f"Exception: parsing of {REQUIRED_GALLERY_FILE_GALLERY} failed for {gallery_xml_path}\n{inst}")
        return None
