from os import path
import xml.etree.ElementTree as XmlEt
from collections.abc import Callable
from .gallery_configuration import GALLERY_XML_IMAGES_TAG, GALLERY_XML_IMAGES_ALT_TAG, \
    GALLERY_XML_IMAGES_ALTDE_TAG, REQUIRED_GALLERY_FILE_GALLERY, GALLERY_XML_IMAGES_FILENAME_TAG, \
    GALLERY_XML_IMAGES_CAPTION_TAG, GALLERY_XML_IMAGES_PRINTS_TAG

IMAGE_ELEMENT_BLUEPRINT = f'''<image>
<{GALLERY_XML_IMAGES_FILENAME_TAG}></{GALLERY_XML_IMAGES_FILENAME_TAG}>
<{GALLERY_XML_IMAGES_CAPTION_TAG}></{GALLERY_XML_IMAGES_CAPTION_TAG}>
<{GALLERY_XML_IMAGES_ALT_TAG}></{GALLERY_XML_IMAGES_ALT_TAG}>
<{GALLERY_XML_IMAGES_ALTDE_TAG}></{GALLERY_XML_IMAGES_ALTDE_TAG}>
<{GALLERY_XML_IMAGES_PRINTS_TAG}></{GALLERY_XML_IMAGES_PRINTS_TAG}>
</image>'''


def read_gallery_xml(folder: str) -> str:
    with open(path.join(folder, REQUIRED_GALLERY_FILE_GALLERY)) as f:
        contents = f.read()
    return contents


def parse_gallery_xml(xml_data: str) -> XmlEt.Element | None:
    try:
        gallery_element = XmlEt.fromstring(xml_data)
        if get_images_element(gallery_element) is None:
            return None
        return gallery_element
    except XmlEt.ParseError:
        return None


def extract_filename_from_image_element(element: XmlEt.Element) -> str | None:
    filename_element = element.find(GALLERY_XML_IMAGES_FILENAME_TAG)
    if filename_element is None:
        return None
    return filename_element.text


def get_images_element(gallery_element: XmlEt.Element) -> XmlEt.Element | None:
    return gallery_element.find(GALLERY_XML_IMAGES_TAG)


def get_image_element_filenames_list(gallery_element: XmlEt.Element) -> list[str]:
    xmlImages = []
    for image_element in get_images_element(gallery_element):
        file_name = extract_filename_from_image_element(image_element)
        if file_name is not None:
            xmlImages.append(file_name)
    return xmlImages


def print_images_list(gallery_element: XmlEt.Element):
    images_element = get_images_element(gallery_element)
    for i, images_element in enumerate(images_element):
        print(
            f"  [{i}] - {extract_filename_from_image_element(images_element)}")


def create_image_element(image_name, caption, alt, altDe, size):
    new_xml_image_element = XmlEt.fromstring(IMAGE_ELEMENT_BLUEPRINT)

    xml_filename = new_xml_image_element.find(
        GALLERY_XML_IMAGES_FILENAME_TAG)
    xml_filename.text = image_name

    xml_caption = new_xml_image_element.find(
        GALLERY_XML_IMAGES_CAPTION_TAG)
    xml_caption.text = caption

    xml_alt = new_xml_image_element.find(
        GALLERY_XML_IMAGES_ALT_TAG)
    xml_alt.text = alt

    xml_altDe = new_xml_image_element.find(
        GALLERY_XML_IMAGES_ALTDE_TAG)
    xml_altDe.text = altDe

    xml_prints = new_xml_image_element.find(
        GALLERY_XML_IMAGES_PRINTS_TAG)
    if size == "1":
        xml_prints.set("size", "small")
    elif size == "2":
        xml_prints.set("size", "medium")
    else:
        xml_prints.set("size", "large")

    return new_xml_image_element


def update_image_descriptions(images_element: XmlEt.Element, image_callback: Callable[[str, str], None] | None = None):
    for image_element in images_element:
        image_name = extract_filename_from_image_element(
            image_element)
        print(f"\n{image_name}:")
        alt_element = image_element.find(GALLERY_XML_IMAGES_ALT_TAG)
        altde_element = image_element.find(
            GALLERY_XML_IMAGES_ALTDE_TAG)

        if alt_element is None:
            alt_element = XmlEt.SubElement(image_element, "alt")

        if alt_element.text is None or len(alt_element.text) == 0:
            alt_element.text = input("-> Please provide a description: ")

        if image_callback is not None and len(alt_element.text) > 0:
            image_callback(image_name, alt_element.text)

        if altde_element is None:
            altde_element = XmlEt.SubElement(image_element, "altDe")

        if altde_element.text is None or len(altde_element.text) == 0:
            altde_element.text = input(
                "-> Please provide a german description: ")


def write_formatted_xml(gallery_element: XmlEt.Element, gallery_folder):
    """Write a formatted Gallery XML"""
    xml_gallery_path = path.join(gallery_folder, REQUIRED_GALLERY_FILE_GALLERY)
    XmlEt.indent(gallery_element)
    XmlEt.ElementTree(gallery_element).write(xml_gallery_path)
