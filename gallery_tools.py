import os

SUPPORTED_IMAGE_FORMATS = (".jpg", ".jpeg")


def get_list_of_supported_images_in_folder(folder):
    files = os.listdir(folder)
    return [file for file in files if file.endswith(SUPPORTED_IMAGE_FORMATS)]
