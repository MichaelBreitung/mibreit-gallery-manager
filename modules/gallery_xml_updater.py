from os import path, remove
import xml.etree.ElementTree as XmlEt
from .gallery_tools import get_list_of_supported_images_in_folder
from .gallery_configuration import GALLERY_XML_IMAGES_TAG, REQUIRED_GALLERY_FILE_GALLERY, REQUIRED_GALLERY_FOLDER_IMAGES, GALLERY_XML_IMAGES_FILENAME_TAG
from .gallery_image_element import GalleryImageElement
from .gallery_tools import parse_gallery_xml


class GalleryXmlUpdater:
    __images_path = None
    __images_set = None
    __gallery_xml_path = None
    __images_in_gallery_set = None
    __xml_gallery_tree = None

    def __init__(self, images_path, gallery_xml_path):
        self.__images_path = images_path
        self.__gallery_xml_path = gallery_xml_path
        self.__images_set = self.__images_set = set(get_list_of_supported_images_in_folder(
            images_path))

    def __extract_filename_from_xml_image_element(self, element: XmlEt.ElementTree):
        return element.find(GALLERY_XML_IMAGES_FILENAME_TAG).text

    def __get_list_of_images_from_gallery(self):
        xmlImages = map(self.__extract_filename_from_xml_image_element,
                        self.__xml_gallery_tree.getroot().find(GALLERY_XML_IMAGES_TAG))
        return xmlImages

    def __update_gallery_images_set(self):
        self.__images_in_gallery_set = set(
            self.__get_list_of_images_from_gallery())

    def __select_image_position(self, xml_images_element):
        for i, xml_image_element in enumerate(xml_images_element):
            print(
                f"  [{i}] - {self.__extract_filename_from_xml_image_element(xml_image_element)}")
        return int(input(f"-> At which index shall the image be inserted? "))

    def __synchronize_gallery_elements(self, missing_gallery_elements, superfluous_gallery_elements):
        xml_images_element = self.__xml_gallery_tree.getroot().find(GALLERY_XML_IMAGES_TAG)
        xml_image_elements_to_remove = []
        # check for images to remove from gallery
        for xml_image_element in xml_images_element:
            image_name = self.__extract_filename_from_xml_image_element(
                xml_image_element)
            if image_name in superfluous_gallery_elements:
                print(f"\n{image_name}:")
                response = input(
                    f"-> Image is present in {REQUIRED_GALLERY_FILE_GALLERY}, but not in {REQUIRED_GALLERY_FOLDER_IMAGES}. Shall it be removed from {REQUIRED_GALLERY_FILE_GALLERY}? (yes/no) ")
                if response in ("yes", "y"):
                    print(
                        f"-> Removing image {image_name} from {REQUIRED_GALLERY_FILE_GALLERY}")
                    xml_image_elements_to_remove.append(xml_image_element)

        for xml_image_element in xml_image_elements_to_remove:
            xml_images_element.remove(xml_image_element)

        # check for images to remove from images folder
        for image_name in missing_gallery_elements:
            print(f"\n{image_name}:")
            response = input(
                f"-> Image is present in {REQUIRED_GALLERY_FOLDER_IMAGES}, but not in {REQUIRED_GALLERY_FILE_GALLERY}. Shall it be removed from {REQUIRED_GALLERY_FOLDER_IMAGES}? (yes/no) ")
            if response in ("yes", "y"):
                print(
                    f"-> Removing image {image_name} from {REQUIRED_GALLERY_FOLDER_IMAGES}")
                remove(path.join(self.__images_path, image_name))
            else:
                response = input(
                    f"-> Shall it instead be created inside {REQUIRED_GALLERY_FILE_GALLERY}? (yes/no) ")
                if response in ("yes", "y"):
                    caption = input(f"-> Please provide a caption: ")
                    alt = input(f"-> Please provide a description: ")
                    altGer = input(f"-> Please provide a german description: ")
                    size = input(
                        f"-> Please provide a maximum print size (1 - up to 45cm; 2 - up to 60cm; 3 - up to 90cm): ")
                    index = self.__select_image_position(xml_images_element)
                    new_xml_image_element = GalleryImageElement(
                        image_name, caption, alt, altGer, size).create()
                    xml_images_element.insert(index, new_xml_image_element)

    def update(self):
        self.__xml_gallery_tree = parse_gallery_xml(self.__gallery_xml_path)
        if self.__xml_gallery_tree != None:
            self.__update_gallery_images_set()

            missing_gallery_elements = self.__images_set - self.__images_in_gallery_set
            superfluous_gallery_elements = self.__images_in_gallery_set - self.__images_set

            self.__synchronize_gallery_elements(
                missing_gallery_elements, superfluous_gallery_elements)
            XmlEt.indent(self.__xml_gallery_tree.getroot())
            self.__xml_gallery_tree.write(self.__gallery_xml_path)
            return True
        else:
            return False
