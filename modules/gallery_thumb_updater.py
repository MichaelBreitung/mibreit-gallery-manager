import os
from .gallery_tools import get_list_of_supported_images_in_folder
from .gallery_thumb_creator import GalleryThumbCreator


class GalleryThumbUpdater:

    def __init__(self, images_path: str, thumbs_path: str):
        self.__thumb_creator = GalleryThumbCreator(images_path, thumbs_path)
        images_list = get_list_of_supported_images_in_folder(images_path)
        thumbs_list = get_list_of_supported_images_in_folder(thumbs_path)
        self.__images_set = set(images_list)
        self.__thumbs_path = thumbs_path
        self.__thumbs_set = set(thumbs_list)

    def __create_missing_thumbs(self, missing_thumbs_set: set[str]):
        for thumb_name in missing_thumbs_set:
            print(f"\n{thumb_name}: Creating missing thumb")
            self.__thumb_creator.create(thumb_name)

    def __remove_superfluous_thumbs(self, superfluous_thumbs_list: set[str]):
        for thumb_name in superfluous_thumbs_list:
            print(f"\n{thumb_name}: Removing superfluous thumb")
            os.remove(os.path.join(self.__thumbs_path, thumb_name))

    def update(self):
        missing_thumbs_set = self.__images_set - self.__thumbs_set
        superfluous_thumbs_set = self.__thumbs_set - self.__images_set

        if len(missing_thumbs_set):
            self.__create_missing_thumbs(missing_thumbs_set)

        if len(superfluous_thumbs_set):
            self.__remove_superfluous_thumbs(superfluous_thumbs_set)
