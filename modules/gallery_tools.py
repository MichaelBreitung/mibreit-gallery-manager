from os import listdir
from .gallery_configuration import REQUIRED_GALLERY_ELEMENTS

SUPPORTED_IMAGE_FORMATS = (".jpg", ".jpeg")


def get_list_of_supported_images_in_folder(folder):
    files = listdir(folder)
    return [file for file in files if file.endswith(SUPPORTED_IMAGE_FORMATS)]


def is_gallery_path(path):
    return REQUIRED_GALLERY_ELEMENTS <= set(listdir(path))
