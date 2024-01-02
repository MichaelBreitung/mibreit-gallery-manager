from os import path
from PIL import Image, ImageEnhance
from .gallery_configuration import THUMB_QUALITY, THUMB_SHARPEN_FACTOR, THUMBNAIL_SIZE
from .gallery_variant_creator import GalleryVariantCreator

class GalleryThumbCreator(GalleryVariantCreator):
    def __init__(self, images_path: str, thumbs_path: str):
        self.__images_path = images_path
        self.__thumbs_path = thumbs_path

    def create(self, variant_name: str):
        thumb = Image.open(path.join(
            self.__images_path, variant_name)).copy()
        thumb.thumbnail(THUMBNAIL_SIZE, Image.LANCZOS)
        thumb = ImageEnhance.Sharpness(thumb).enhance(THUMB_SHARPEN_FACTOR)
        thumb.save(path.join(self.__thumbs_path,
                             variant_name), quality=THUMB_QUALITY)
