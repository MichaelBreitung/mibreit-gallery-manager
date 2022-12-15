import os
import xml.etree.ElementTree as XmlEt
from PIL import Image, ImageEnhance
from gallery_image_element import GalleryImageElement

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

THUMB_SHARPEN_FACTOR = 1.5
THUMB_QUALITY = 70

def is_gallery_path(path):
    return REQUIRED_GALLERY_ELEMENTS <= set(os.listdir(path))

def synchronize_gallery(path):
    if is_gallery_path(path):
        gallery_sync = GallerySynchronizer(path)
        gallery_sync.synchronize()

class GallerySynchronizer:
    __gallery_path = None
    __images_path = None
    __images_set = None
    __thumbs_path = None
    __thumbs_set = None
    __gallery_xml_path = None
    __images_in_gallery_set = None
    __xml_gallery_tree = None

    def __init__(self, abs_gallery_path):
        self.__gallery_path = abs_gallery_path
        self.__images_path = os.path.join(
            abs_gallery_path, REQUIRED_GALLERY_FOLDER_IMAGES)
        self.__thumbs_path = os.path.join(
            abs_gallery_path, REQUIRED_GALLERY_FOLDER_SMALL)
        self.__gallery_xml_path = os.path.join(
            abs_gallery_path, REQUIRED_GALLERY_FILE_GALLERY)

    def __parse_gallery_xml(self):
        try:
            self.__xml_gallery_tree = XmlEt.parse(self.__gallery_xml_path)
            # making the following check will ensure that other methods in this class work properly
            return self.__xml_gallery_tree.getroot().find(GALLERY_XML_IMAGES_TAG) is not None
        except Exception as inst:
            print(
                f"Exception: parsing of {REQUIRED_GALLERY_FILE_GALLERY} failed for {self.__gallery_path}\n{inst}")
            return False
        
    def __get_list_of_supported_images_in_folder(self, path):
        files = os.listdir(path)
        return [file for file in files if file.endswith(SUPPORTED_IMAGE_FORMATS)]

    def __update_images_set(self):
        self.__images_set = set(self.__get_list_of_supported_images_in_folder(
            os.path.join(self.__gallery_path, REQUIRED_GALLERY_FOLDER_IMAGES)))

    def __update_thumbs_set(self):
        self.__thumbs_set = set(self.__get_list_of_supported_images_in_folder(
            os.path.join(self.__gallery_path, REQUIRED_GALLERY_FOLDER_SMALL)))

    def __extract_filename_from_xml_image_element(self, element: XmlEt.ElementTree):
        return element.find(GALLERY_XML_IMAGES_FILENAMW_TAG).text

    def __get_list_of_images_from_gallery(self):
        xmlImages = map(self.__extract_filename_from_xml_image_element,
                        self.__xml_gallery_tree.getroot().find(GALLERY_XML_IMAGES_TAG))
        return xmlImages

    def __update_gallery_images_set(self):
        self.__images_in_gallery_set = set(
            self.__get_list_of_images_from_gallery())

    def __create_missing_thumbs(self, missing_thumbs_set):
        for thumb_name in missing_thumbs_set:
            print(f"Creating missing thumb -> {thumb_name}")
            thumb = Image.open(os.path.join(
                self.__images_path, thumb_name)).copy()
            thumb.thumbnail(THUMBNAIL_SIZE, Image.LANCZOS)
            thumb = ImageEnhance.Sharpness(thumb).enhance(THUMB_SHARPEN_FACTOR)
            thumb.save(os.path.join(self.__thumbs_path, thumb_name),quality=THUMB_QUALITY)

    def __remove_superfluous_thumbs(self, superfluous_thumbs_list):
        for thumb_name in superfluous_thumbs_list:
            print(f"Removing superfluous thumb -> {thumb_name}")
            os.remove(os.path.join(self.__thumbs_path, thumb_name))

    def __synchronize_gallery_elements(self, missing_gallery_elements, superfluous_gallery_elements):
        xml_images_element = self.__xml_gallery_tree.getroot().find(GALLERY_XML_IMAGES_TAG)
        # check for images to remove from gallery
        for xml_image_element in xml_images_element:
            image_name = self.__extract_filename_from_xml_image_element(
                xml_image_element)
            if image_name in superfluous_gallery_elements:
                response = input(
                    f"The image {image_name} is present in {REQUIRED_GALLERY_FILE_GALLERY}, but not in {REQUIRED_GALLERY_FOLDER_IMAGES}. Shall it be removed from {REQUIRED_GALLERY_FILE_GALLERY}? (yes/no) ")
                if response in ("yes","y"):
                    print(
                        f"Removing image {image_name} from {REQUIRED_GALLERY_FILE_GALLERY}")
                    xml_images_element.remove(xml_image_element)
        # check for images to remove from images folder
        for image_name in missing_gallery_elements:
            response = input(
                f"The image {image_name} is present in {REQUIRED_GALLERY_FOLDER_IMAGES}, but not in {REQUIRED_GALLERY_FILE_GALLERY}. Shall it be removed from {REQUIRED_GALLERY_FOLDER_IMAGES}? (yes/no) ")
            if response in ("yes","y"):
                print(
                    f"Removing image {image_name} from {REQUIRED_GALLERY_FOLDER_IMAGES}")
                os.remove(os.path.join(self.__images_path, image_name))
            else:
                response = input(
                    f"Shall it instead be created inside {REQUIRED_GALLERY_FILE_GALLERY}? (yes/no) ")
                if response in ("yes","y"):
                    new_xml_image_element = GalleryImageElement(image_name)
                    new_xml_image_element.create(xml_images_element)

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
        else:
            print(f"Invalid Gallery under {self.__gallery_path}. The {REQUIRED_GALLERY_FILE_GALLERY} is invalid.")
