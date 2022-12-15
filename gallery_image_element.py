import xml.etree.ElementTree as XmlEt
from gallery_configuration import GALLERY_XML_IMAGES_FILENAME_TAG, GALLERY_XML_IMAGES_CAPTION_TAG, GALLERY_XML_IMAGES_PRINTS_TAG

image_element_blueprint = '''<image>
<filename></filename>
<caption></caption>
<prints size="large"></prints>
</image>
'''


class GalleryImageElement:
    def __init__(self, image_name):
        self.__image_name = image_name

    def create(self):
        new_xml_image_element = XmlEt.fromstring(image_element_blueprint)

        xml_filename = new_xml_image_element.find(
            GALLERY_XML_IMAGES_FILENAME_TAG)
        xml_filename.text = self.__image_name

        caption = input(f"-> Please provide a caption: ")
        xml_caption = new_xml_image_element.find(
            GALLERY_XML_IMAGES_CAPTION_TAG)
        xml_caption.text = caption

        size = input(
            f"-> Please provide a maximum print size (1 - up to 45cm; 2 - up to 60cm; 3 - up to 90cm): ")
        xml_prints = new_xml_image_element.find(
            GALLERY_XML_IMAGES_PRINTS_TAG)
        if size == "1":
            xml_prints.set("size", "small")
        elif size == "2":
            xml_prints.set("size", "medium")
        else:
            xml_prints.set("size", "large")

        return new_xml_image_element
