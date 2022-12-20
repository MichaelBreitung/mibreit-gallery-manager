from os import path
from .gallery_configuration import REQUIRED_GALLERY_FILE_GALLERY, REQUIRED_GALLERY_FOLDER_IMAGES
from .gallery_tools import is_gallery_path
from .gallery_image_descriptions_updater import GalleryImageDescriptionsUpdater


def update_image_descriptions(path):
    if is_gallery_path(path):
        gallery_sync = GalleryImageDescriptions(path)
        gallery_sync.update()


class GalleryImageDescriptions:
    __gallery_path = None
    __images_path = None
    __gallery_xml_path = None

    def __init__(self, abs_gallery_path):
        self.__gallery_path = abs_gallery_path
        self.__images_path = path.join(
            abs_gallery_path, REQUIRED_GALLERY_FOLDER_IMAGES)
        self.__gallery_xml_path = path.join(
            self.__gallery_path, REQUIRED_GALLERY_FILE_GALLERY)

    def update(self):
        print("\nUpdating image descriptions in gallery -> ", self.__gallery_path)
        GalleryImageDescriptionsUpdater(
            self.__images_path, self.__gallery_xml_path).update()
