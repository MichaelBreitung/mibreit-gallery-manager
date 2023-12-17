from os import path
import xml.etree.ElementTree as XmlEt
from collections.abc import Callable
from .gallery_configuration import GALLERY_XML_IMAGES_TAG, GALLERY_XML_IMAGES_ALT_TAG, \
    GALLERY_XML_IMAGES_ALTDE_TAG, REQUIRED_GALLERY_FILE_GALLERY, GALLERY_XML_IMAGES_FILENAME_TAG, \
    GALLERY_XML_IMAGES_CAPTION_TAG, GALLERY_XML_IMAGES_PRINTS_TAG, GALLERY_XML_CONTENT_TAG, \
    GALLERY_XML_INFO_TAG, GALLERY_XML_INFODE_TAG

IMAGE_ELEMENT_BLUEPRINT = f'''<image>
<{GALLERY_XML_IMAGES_FILENAME_TAG}/>
<{GALLERY_XML_IMAGES_CAPTION_TAG}/>
<{GALLERY_XML_IMAGES_ALT_TAG}/>
<{GALLERY_XML_IMAGES_ALTDE_TAG}/>
<{GALLERY_XML_IMAGES_PRINTS_TAG}/>
</image>'''


def read_gallery_xml(folder: str) -> str:
    with open(path.join(folder, REQUIRED_GALLERY_FILE_GALLERY)) as f:
        contents = f.read()
    return contents


def parse_gallery_xml(xml_data: str) -> XmlEt.Element | None:
    try:
        gallery_element = XmlEt.fromstring(xml_data)
        if gallery_element.find(GALLERY_XML_IMAGES_TAG) is None:
            return None
        return gallery_element
    except XmlEt.ParseError:
        return None


def extract_filename_from_image_element(element: XmlEt.Element) -> str | None:
    filename_element = element.find(GALLERY_XML_IMAGES_FILENAME_TAG)
    if filename_element is None:
        return None
    return filename_element.text


def get_images_element(gallery_element: XmlEt.Element) -> XmlEt.Element:
    images_element = gallery_element.find(GALLERY_XML_IMAGES_TAG)
    if images_element is None:
        create_images_element(gallery_element)
        images_element = gallery_element.find(GALLERY_XML_IMAGES_TAG)

    return images_element  # type: ignore


def create_images_element(gallery_element: XmlEt.Element):
    XmlEt.SubElement(gallery_element, GALLERY_XML_IMAGES_TAG)


def get_info_element(gallery_element: XmlEt.Element, ger: bool = False) -> XmlEt.Element:
    info_element = None
    if ger:
        info_element = gallery_element.find(GALLERY_XML_INFODE_TAG)
        if info_element is None:
            create_info_element(gallery_element)
            info_element = gallery_element.find(GALLERY_XML_INFODE_TAG)
    else:
        info_element = gallery_element.find(GALLERY_XML_INFO_TAG)
        if info_element is None:
            create_info_element(gallery_element)
            info_element = gallery_element.find(GALLERY_XML_INFO_TAG)

    return info_element  # type: ignore


def create_info_element(gallery_element: XmlEt.Element, ger: bool = False):
    XmlEt.SubElement(gallery_element, GALLERY_XML_INFO_TAG)


def get_image_element_filenames_list(gallery_element: XmlEt.Element) -> list[str]:
    xmlImages = []
    images_element = get_images_element(gallery_element)
    for image_element in images_element:
        file_name = extract_filename_from_image_element(image_element)
        if file_name is not None:
            xmlImages.append(file_name)
    return xmlImages


def print_images_list(gallery_element: XmlEt.Element):
    images_element = get_images_element(gallery_element)
    for i, images_element in enumerate(images_element):
        print(
            f"  [{i}] - {extract_filename_from_image_element(images_element)}")


def create_image_element(image_name: str) -> XmlEt.Element:
    new_xml_image_element = XmlEt.fromstring(IMAGE_ELEMENT_BLUEPRINT)

    xml_filename = new_xml_image_element.find(
        GALLERY_XML_IMAGES_FILENAME_TAG)
    xml_filename.text = image_name  # type: ignore

    return new_xml_image_element


def update_image_description(image_element: XmlEt.Element, image_name: str, image_callback: Callable[[str, str, str], None] | None = None):   
    alt_element = image_element.find(GALLERY_XML_IMAGES_ALT_TAG)
    altde_element = image_element.find(
        GALLERY_XML_IMAGES_ALTDE_TAG)
    caption_element = image_element.find(
        GALLERY_XML_IMAGES_CAPTION_TAG)
    xml_prints = image_element.find(
        GALLERY_XML_IMAGES_PRINTS_TAG)
        
    if xml_prints is None:
        xml_prints = XmlEt.SubElement(image_element, GALLERY_XML_IMAGES_PRINTS_TAG)

    if xml_prints.get("size") is None:
        size = input("-> Please provide a maximum print size (1 - up to 45cm; 2 - up to 60cm; 3 - up to 90cm): ")
        if size == "1":
            xml_prints.set("size", "small")  # type: ignore
        elif size == "2":
            xml_prints.set("size", "medium")  # type: ignore
        else:
            xml_prints.set("size", "large")  # type: ignore

    if caption_element is None:
        caption_element = XmlEt.SubElement(
            image_element, GALLERY_XML_IMAGES_CAPTION_TAG)

    if caption_element.text is None or len(caption_element.text) == 0:
        caption_element.text = input("-> Please provide a caption: ")

    if alt_element is None:
        alt_element = XmlEt.SubElement(
            image_element, GALLERY_XML_IMAGES_ALT_TAG)

    if alt_element.text is None or len(alt_element.text) == 0:
        alt_element.text = input("-> Please provide a description: ")

    if image_callback is not None and len(alt_element.text) > 0 and len(caption_element.text):
        image_callback(image_name, caption_element.text,
                       alt_element.text)

    if altde_element is None:
        altde_element = XmlEt.SubElement(
            image_element, GALLERY_XML_IMAGES_ALTDE_TAG)

    if altde_element.text is None or len(altde_element.text) == 0:
        altde_element.text = input(
            "-> Please provide a german description: ")


def update_image_descriptions(images_element: XmlEt.Element, image_callback: Callable[[str, str, str], None] | None = None):
    invalid_image_elements = []
    for image_element in images_element:
        image_name = extract_filename_from_image_element(
            image_element)
        if image_name is not None:
            print(f"\n{image_name}:")
            update_image_description(image_element, image_name, image_callback)
        else:
            invalid_image_elements.append(image_element)

        for invalid_image_element in invalid_image_elements:
            images_element.remove(invalid_image_element)


def update_gallery_description(info_en: XmlEt.Element, info_de: XmlEt.Element):
    content_element = info_en.find(GALLERY_XML_CONTENT_TAG)
    if content_element is None:
        content_element = XmlEt.SubElement(
            info_en, GALLERY_XML_CONTENT_TAG)

    if content_element.text is None or len(content_element.text) == 0:
        content_element.text = input(
            "-> Please provide information about gallery content: ")

    content_element = info_de.find(GALLERY_XML_CONTENT_TAG)
    if content_element is None:
        content_element = XmlEt.SubElement(
            info_de, GALLERY_XML_CONTENT_TAG)

    if content_element.text is None or len(content_element.text) == 0:
        content_element.text = input(
            "-> Please provide information about gallery content in German: ")


def write_formatted_xml(gallery_element: XmlEt.Element, gallery_folder: str):
    """Write a formatted Gallery XML"""
    xml_gallery_path = path.join(gallery_folder, REQUIRED_GALLERY_FILE_GALLERY)
    XmlEt.indent(gallery_element)
    XmlEt.ElementTree(gallery_element).write(xml_gallery_path)
