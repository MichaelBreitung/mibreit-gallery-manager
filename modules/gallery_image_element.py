import xml.etree.ElementTree as XmlEt
from .gallery_configuration import GALLERY_XML_IMAGES_FILENAME_TAG, GALLERY_XML_IMAGES_CAPTION_TAG, GALLERY_XML_IMAGES_ALT_TAG, GALLERY_XML_IMAGES_ALTDE_TAG, GALLERY_XML_IMAGES_PRINTS_TAG

image_element_blueprint = '''<image>
<filename></filename>
<caption></caption>
<alt></alt>
<altDe></altDe>
<prints></prints>
</image>'''


class GalleryImageElement:
    def __init__(self, image_name, caption, alt, altDe, size):
        self.__image_name = image_name
        self.__caption = caption
        self.__alt = alt
        self.__altDe = altDe
        self.__size = size

    def create(self):
        new_xml_image_element = XmlEt.fromstring(image_element_blueprint)

        xml_filename = new_xml_image_element.find(
            GALLERY_XML_IMAGES_FILENAME_TAG)
        xml_filename.text = self.__image_name

        xml_caption = new_xml_image_element.find(
            GALLERY_XML_IMAGES_CAPTION_TAG)
        xml_caption.text = self.__caption

        xml_alt = new_xml_image_element.find(
            GALLERY_XML_IMAGES_ALT_TAG)
        xml_alt.text = self.__alt

        xml_altDe = new_xml_image_element.find(
            GALLERY_XML_IMAGES_ALTDE_TAG)
        xml_altDe.text = self.__altDe

        xml_prints = new_xml_image_element.find(
            GALLERY_XML_IMAGES_PRINTS_TAG)
        if self.__size == "1":
            xml_prints.set("size", "small")
        elif self.__size == "2":
            xml_prints.set("size", "medium")
        else:
            xml_prints.set("size", "large")

        return new_xml_image_element
