import os
from .gallery_tools import get_list_of_supported_images_in_folder
from .gallery_thumb_creator import GalleryThumbCreator
from .gallery_variant_creator import GalleryVariantCreator
from .gallery_configuration import MEDIUM_QUALITY, MEDIUM_SHARPEN_FACTOR, MEDIUM_WIDTH

class GalleryVariantsUpdater:

    def __init__(self, images_path: str, variant_path: str, is_thumb: bool = True):
        self.__variant_creator = GalleryThumbCreator(images_path, variant_path) if is_thumb else GalleryVariantCreator(images_path, variant_path, MEDIUM_WIDTH, MEDIUM_SHARPEN_FACTOR, MEDIUM_QUALITY)
        images_list = get_list_of_supported_images_in_folder(images_path)
        os.makedirs(variant_path, exist_ok=True)
        variant_images_list = get_list_of_supported_images_in_folder(variant_path)
        self.__images_set = set(images_list)
        self.__variant_path = variant_path
        self.__variant_images_set = set(variant_images_list)

    def __create_missing_variant(self, missing_variant_images_set: set[str]):
        for variant_image_name in missing_variant_images_set:
            print(f"\n{variant_image_name}: Creating missing image")

            self.__variant_creator.create(variant_image_name)

    def __remove_superfluous_variant(self, superfluous_thumbs_list: set[str]):
        for thumb_name in superfluous_thumbs_list:
            print(f"\n{thumb_name}: Removing superfluous thumb")
            os.remove(os.path.join(self.__variant_path, thumb_name))

    def update(self):
        missing_variant_images_set = self.__images_set - self.__variant_images_set
        superfluous_variant_images_set = self.__variant_images_set - self.__images_set

        if len(missing_variant_images_set):
            self.__create_missing_variant(missing_variant_images_set)

        if len(superfluous_variant_images_set):
            self.__remove_superfluous_variant(superfluous_variant_images_set)
