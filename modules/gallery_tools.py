from os import path, listdir, getcwd
from PIL import Image
from PIL.ExifTags import Base
from .gallery_configuration import REQUIRED_GALLERY_ELEMENTS, REQUIRED_GALLERY_FOLDER_IMAGES, \
    REQUIRED_GALLERY_FOLDER_SMALL

SUPPORTED_IMAGE_FORMATS = (".jpg", ".jpeg")


def get_list_of_supported_images_in_folder(folder: str) -> list[str]:
    """Returns a lit of the supported images"""
    files = listdir(folder)
    return [file for file in files if file.endswith(SUPPORTED_IMAGE_FORMATS)]


def is_gallery_path(folder: str) -> bool:
    """Returns True if a folder contains a gallery"""
    return REQUIRED_GALLERY_ELEMENTS <= set(listdir(folder))


def get_valid_path(folder: str) -> str:
    """
    Normalize the given folder and return either absolute or relative path
    that is checked to lead to a proper folder
    """
    valid_path = path.normcase(folder)

    if not path.isdir(valid_path):
        valid_path = path.normpath(
            path.join(getcwd(), valid_path))

    if not path.isdir(valid_path):
        raise ValueError(f"Invalid folder: {folder}")

    return valid_path


def get_images_path(folder: str) -> str:
    """Returns images path within given gallery folder"""
    return path.join(folder, REQUIRED_GALLERY_FOLDER_IMAGES)


def get_thumbs_path(folder: str) -> str:
    """Returns thumbs path within given gallery folder"""
    return path.join(folder, REQUIRED_GALLERY_FOLDER_SMALL)


def update_image_exif_data(images_folder, image_name: str, description: str):
    """Updates the description EXIF data for given image"""
    image_path = path.join(images_folder, image_name)
    image_data = Image.open(image_path)
    if image_data is not None:
        exif_data = image_data.getexif()
        exif_data[Base.ImageDescription.value] = description
        image_data.save(image_path, exif=exif_data)
