import os
import xml.etree.ElementTree as XmlEt
from PIL import Image


# global constants
REQUIRED_GALLERY_FOLDER_IMAGES = "images"
REQUIRED_GALLERY_FOLDER_SMALL = "small"
REQUIRED_GALLERY_FILE_GALLERY = "gallery.xml"
REQUIRED_GALLERY_ELEMENTS = {REQUIRED_GALLERY_FILE_GALLERY,
                             REQUIRED_GALLERY_FOLDER_IMAGES, REQUIRED_GALLERY_FOLDER_SMALL}
SUPPORTED_IMAGE_FORMATS = (".jpg", ".jpeg")
THUMBNAIL_SIZE = (200, 200)
GALLERY_XML_IMAGES_TAG = "images"
GALLERY_XML_IMAGES_FILENAMW_TAG = "filename"

def is_gallery_path(path):
    return REQUIRED_GALLERY_ELEMENTS <= set(os.listdir(path))

class GallerySynchronizer:
    def __init__(self, abs_gallery_path):
        self.__gallery_path = abs_gallery_path
        self.__images_path = os.path.join(
            abs_gallery_path, REQUIRED_GALLERY_FOLDER_IMAGES)
        self.__thumbs_path = os.path.join(
            abs_gallery_path, REQUIRED_GALLERY_FOLDER_SMALL)
        self.__gallery_xml_path = os.path.join(
            abs_gallery_path, REQUIRED_GALLERY_FILE_GALLERY)

    def __extract_filename_from_image_element(self, element: XmlEt.ElementTree):
        return element.find(GALLERY_XML_IMAGES_FILENAMW_TAG).text

    def __parse_gallery_xml(self):
        try:
            self.__xml_gallery_tree = XmlEt.parse(self.__gallery_xml_path)
            return True
        except Exception as inst:
            print(
                f"Exception: parsing of {REQUIRED_GALLERY_FILE_GALLERY} failed for {self.__gallery_path}\n{inst}")
            return False

    def __update_images_set(self):
        self.__images_set = set(self.__get_list_of_supported_images_from_path(
            os.path.join(self.__gallery_path, REQUIRED_GALLERY_FOLDER_IMAGES)))

    def __update_thumbs_set(self):
        self.__thumbs_set = set(self.__get_list_of_supported_images_from_path(
            os.path.join(self.__gallery_path, REQUIRED_GALLERY_FOLDER_SMALL)))

    def __update_gallery_images_set(self):
        self.__images_in_gallery_set = set(
            self.__get_list_of_images_from_gallery())

    def __get_list_of_supported_images_from_path(self, path):
        files = os.listdir(path)
        return [file for file in files if file.endswith(SUPPORTED_IMAGE_FORMATS)]

    def __get_list_of_images_from_gallery(self):
        xmlImages = map(self.__extract_filename_from_image_element,
                        self.__xml_gallery_tree.getroot().find(GALLERY_XML_IMAGES_TAG))
        return xmlImages

    def __create_missing_thumbs(self, missing_thumbs_set):
        for thumb_name in missing_thumbs_set:
            print(f"creating missing thumb -> {thumb_name}")
            thumb = Image.open(os.path.join(
                self.__images_path, thumb_name)).copy()
            thumb.thumbnail(THUMBNAIL_SIZE)
            thumb.save(os.path.join(self.__thumbs_path, thumb_name))

    def __remove_superfluous_thumbs(self, superfluous_thumbs_list):
        for thumb_name in superfluous_thumbs_list:
            print(f"removing superfluous thumb -> {thumb_name}")
            os.remove(os.path.join(self.__thumbs_path, thumb_name))

    def __synchronize_gallery_elements(self, missing_gallery_elements, superfluous_gallery_elements):
        images_element = self.__xml_gallery_tree.getroot().find(GALLERY_XML_IMAGES_TAG)
        # check for images to remove from gallery
        for image_element in images_element:
            image_name = self.__extract_filename_from_image_element(
                image_element)
            if image_name in superfluous_gallery_elements:
                response = input(
                    f"The image {image_name} is present in {REQUIRED_GALLERY_FILE_GALLERY}, but not in {REQUIRED_GALLERY_FOLDER_IMAGES}. Shall it be removed from {REQUIRED_GALLERY_FILE_GALLERY}? (yes/no) ")
                if response == "yes":
                    images_element.remove(image_element)
        # check for images to remove from images folder
        for image_name in missing_gallery_elements:
            response = input(
                f"The image {image_name} is present in {REQUIRED_GALLERY_FOLDER_IMAGES}, but not in {REQUIRED_GALLERY_FILE_GALLERY}. Shall it be removed from {REQUIRED_GALLERY_FOLDER_IMAGES}? (yes/no) ")
            if response == "yes":
                os.remove(os.path.join(self.__images_path, image_name))
            else:
                response = input(
                    f"Shall it instead be created inside {REQUIRED_GALLERY_FILE_GALLERY}? (yes/no) ")
                # TODO

    def synchronize(self):
        if self.__parse_gallery_xml() == True:
            self.__update_images_set()
            self.__update_thumbs_set()
            self.__update_gallery_images_set()

            # synchronize gallery set with images set
            missing_gallery_elements = self.__images_set - self.__images_in_gallery_set
            superfluous_gallery_elements = self.__images_in_gallery_set - self.__images_set
            self.__synchronize_gallery_elements(
                missing_gallery_elements, superfluous_gallery_elements)
            self.__xml_gallery_tree.write(self.__gallery_xml_path)

            # update of images set required
            self.__update_images_set()

            # synchronize thumbs set with images set
            missing_thumbs_set = self.__images_set - self.__thumbs_set
            superfluous_thumbs_set = self.__thumbs_set - self.__images_set

            if len(missing_thumbs_set):
                self.__create_missing_thumbs(missing_thumbs_set)

            if len(superfluous_thumbs_set):
                self.__remove_superfluous_thumbs(superfluous_thumbs_set)
