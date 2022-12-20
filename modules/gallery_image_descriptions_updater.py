from PIL import Image
from PIL.ExifTags import Base
from os import path
import xml.etree.ElementTree as XmlEt
from .gallery_tools import parse_gallery_xml
from .gallery_configuration import GALLERY_XML_IMAGES_TAG, GALLERY_XML_IMAGES_FILENAME_TAG, GALLERY_XML_IMAGES_ALT_TAG, GALLERY_XML_IMAGES_ALTDE_TAG


class GalleryImageDescriptionsUpdater:
    __images_path = None
    __gallery_xml_path = None
    __xml_gallery_tree = None

    def __init__(self, images_path, gallery_xml_path):
        self.__images_path = images_path
        self.__gallery_xml_path = gallery_xml_path

    def __extract_filename_from_xml_image_element(self, element: XmlEt.ElementTree):
        return element.find(GALLERY_XML_IMAGES_FILENAME_TAG).text

    def __update_image_exif_data(self, image_name, description):
        image_path = path.join(self.__images_path, image_name)
        image_data = Image.open(image_path)
        if image_data != None:
            exif_data = image_data.getexif()
            exif_data[Base.ImageDescription.value] = description
            image_data.save(image_path, exif=exif_data)

    def __update_image_descriptions(self):
        xml_images_element = self.__xml_gallery_tree.getroot().find(GALLERY_XML_IMAGES_TAG)

        for xml_image_element in xml_images_element:
            image_name = self.__extract_filename_from_xml_image_element(
                xml_image_element)
            print(f"\n{image_name}:")
            alt_element = xml_image_element.find(GALLERY_XML_IMAGES_ALT_TAG)
            altDe_element = xml_image_element.find(
                GALLERY_XML_IMAGES_ALTDE_TAG)

            if alt_element == None:
                alt_element = XmlEt.SubElement(xml_image_element, "alt")

            if alt_element.text == None or len(alt_element.text) == 0:
                alt_element.text = input(f"-> Please provide a description: ")

            if len(alt_element.text) > 0:
                self.__update_image_exif_data(image_name, alt_element.text)

            if altDe_element == None:
                altDe_element = XmlEt.SubElement(xml_image_element, "altDe")

            if altDe_element.text == None or len(altDe_element.text) == 0:
                altDe_element.text = input(
                    f"-> Please provide a german description: ")

    def update(self):
        self.__xml_gallery_tree = parse_gallery_xml(self.__gallery_xml_path)
        if self.__xml_gallery_tree != None:
            self.__update_image_descriptions()
            XmlEt.indent(self.__xml_gallery_tree.getroot())
            self.__xml_gallery_tree.write(self.__gallery_xml_path)
            return True
        else:
            return False
