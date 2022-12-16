from os import path
from .gallery_configuration import REQUIRED_GALLERY_FILE_GALLERY, REQUIRED_GALLERY_FOLDER_IMAGES, REQUIRED_GALLERY_FOLDER_SMALL, REQUIRED_GALLERY_ELEMENTS
from .gallery_thumb_updater import GalleryThumbUpdater
from .gallery_xml_updater import GalleryXmlUpdater
from .gallery_tools import is_gallery_path


def synchronize_gallery(path):
    if is_gallery_path(path):
        gallery_sync = GallerySynchronizer(path)
        gallery_sync.synchronize()


class GallerySynchronizer:
    __gallery_path = None
    __images_path = None
    __thumbs_path = None

    def __init__(self, abs_gallery_path):
        self.__gallery_path = abs_gallery_path
        self.__images_path = path.join(
            abs_gallery_path, REQUIRED_GALLERY_FOLDER_IMAGES)
        self.__thumbs_path = path.join(
            self.__gallery_path, REQUIRED_GALLERY_FOLDER_SMALL)
        self.__gallery_xml_path = path.join(
            self.__gallery_path, REQUIRED_GALLERY_FILE_GALLERY)

    def synchronize(self):
        print("\nSynchronizing gallery -> ", self.__gallery_path)
        if GalleryXmlUpdater(self.__images_path, self.__gallery_xml_path).update() is True:
            GalleryThumbUpdater(self.__images_path,
                                self.__thumbs_path).update()
        else:
            print(
                f"Invalid Gallery under {self.__gallery_path}. The {REQUIRED_GALLERY_FILE_GALLERY} is invalid.")
