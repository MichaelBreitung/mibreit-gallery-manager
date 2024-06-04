from os import path
from shutil import copy
from PIL import Image, ImageEnhance


class GalleryVariantCreator:
    def __init__(
        self,
        images_path: str,
        variant_path: str,
        variant_width: int,
        variant_sharpen_factor: float,
        variant_quality: int,
    ):
        self.__images_path = images_path
        self.__variant_path = variant_path
        self.__variant_width = variant_width
        self.__variant_sharpen_factor = variant_sharpen_factor
        self.__variant_quality = variant_quality

    def create(self, variant_name: str):
        variant = Image.open(path.join(self.__images_path, variant_name))

        if variant.width > self.__variant_width:
            aspect = variant.width / variant.height
            variant_height = round(self.__variant_width / aspect)
            resized = variant.resize(
                (self.__variant_width, variant_height), Image.BICUBIC
            )
            resized = ImageEnhance.Sharpness(resized).enhance(
                self.__variant_sharpen_factor
            )
            resized.save(
                path.join(self.__variant_path, variant_name),
                quality=self.__variant_quality,
            )
        else:
            copy(
                path.join(self.__images_path, variant_name),
                path.join(self.__variant_path, variant_name),
            )
