from os import path, remove
from PIL import Image, ImageEnhance
from gallery_tools import get_list_of_supported_images_in_folder
from gallery_configuration import THUMB_QUALITY, THUMB_SHARPEN_FACTOR, THUMBNAIL_SIZE


class GalleryThumbUpdater:
    __images_path = None
    __images_set = None
    __thumbs_path = None
    __thumbs_set = None

    def __init__(self, images_path, thumbs_path):
        self.__images_path = images_path
        self.__images_set = set(get_list_of_supported_images_in_folder(
            images_path))
        self.__thumbs_path = thumbs_path
        self.__thumbs_set = set(get_list_of_supported_images_in_folder(
            thumbs_path))

    def __create_missing_thumbs(self, missing_thumbs_set):
        for thumb_name in missing_thumbs_set:
            print(f"Creating missing thumb -> {thumb_name}")
            thumb = Image.open(path.join(
                self.__images_path, thumb_name)).copy()
            thumb.thumbnail(THUMBNAIL_SIZE, Image.LANCZOS)
            thumb = ImageEnhance.Sharpness(thumb).enhance(THUMB_SHARPEN_FACTOR)
            thumb.save(path.join(self.__thumbs_path,
                       thumb_name), quality=THUMB_QUALITY)

    def __remove_superfluous_thumbs(self, superfluous_thumbs_list):
        for thumb_name in superfluous_thumbs_list:
            print(f"Removing superfluous thumb -> {thumb_name}")
            remove(path.join(self.__thumbs_path, thumb_name))

    def update(self):
        missing_thumbs_set = self.__images_set - self.__thumbs_set
        superfluous_thumbs_set = self.__thumbs_set - self.__images_set

        if len(missing_thumbs_set):
            self.__create_missing_thumbs(missing_thumbs_set)

        if len(superfluous_thumbs_set):
            self.__remove_superfluous_thumbs(superfluous_thumbs_set)
