import unittest
from unittest.mock import patch
import copy
import xml.etree.ElementTree as XmlEt
from modules.gallery_xml_tools import create_image_element, parse_gallery_xml, get_images_element, \
    get_image_element_filenames_list, extract_filename_from_image_element, update_image_descriptions


class TestParseGalleryXml(unittest.TestCase):

    def test_parse_xml_without_images_fails(self):
        self.assertEqual(parse_gallery_xml(
            "<MibreitGallery></MibreitGallery>"), None)

    def test_parse_xml_with_images_succeeds(self):
        test_xml = "<MibreitGallery><images /></MibreitGallery>"
        parsed_xml = parse_gallery_xml(test_xml)
        self.assertIsNotNone(parsed_xml)
        self.assertEqual(XmlEt.tostring(parsed_xml, encoding="unicode"), test_xml) # type: ignore

    def test_get_images_element_succeeds_for_empty_element(self):
        test_xml="<MibreitGallery><images /></MibreitGallery>"
        gallery_element=parse_gallery_xml(test_xml)
        self.assertIsNotNone(gallery_element)
        self.assertEqual(XmlEt.tostring(get_images_element(
            gallery_element), encoding="unicode"), "<images />") # type: ignore

    def test_get_images_element_succeeds_for_list(self):
        test_xml="<MibreitGallery><images><image/></images></MibreitGallery>"
        gallery_element=parse_gallery_xml(test_xml)
        self.assertIsNotNone(gallery_element)
        self.assertEqual(XmlEt.tostring(get_images_element(
            gallery_element), encoding="unicode"), "<images><image /></images>") # type: ignore

    def test_extract_filename_from_empty_image_element(self):
        test_xml="<image></image>"
        image_element=XmlEt.fromstring(test_xml)
        self.assertEqual(
            extract_filename_from_image_element(image_element), None)

    def test_extract_filename_from_image_element(self):
        filename="test"
        test_xml=f"<image><filename>{filename}</filename></image>"
        image_element=XmlEt.fromstring(test_xml)
        self.assertEqual(
            extract_filename_from_image_element(image_element), filename)

    def test_get_image_element_filenames_for_empty_element(self):
        test_xml="<MibreitGallery><images /></MibreitGallery>"
        gallery_element=parse_gallery_xml(test_xml)
        self.assertIsNotNone(gallery_element)
        self.assertEqual(get_image_element_filenames_list(
            gallery_element), []) # type: ignore

    def test_get_image_element_filenames_for_element_without_filename(self):
        test_xml="<MibreitGallery><images><image /></images></MibreitGallery>"
        gallery_element=parse_gallery_xml(test_xml)
        self.assertIsNotNone(gallery_element)
        self.assertEqual(get_image_element_filenames_list(
            gallery_element), []) # type: ignore

    def test_get_image_element_filenames_for_element_with_empty_filename(self):
        test_xml="<MibreitGallery><images><image><filename></filename></image></images></MibreitGallery>"
        gallery_element=parse_gallery_xml(test_xml)
        self.assertIsNotNone(gallery_element)
        self.assertEqual(get_image_element_filenames_list(
            gallery_element), []) # type: ignore

    def test_get_image_element_filenames_for_element_with_filename(self):
        filename="test"
        test_xml=f"<MibreitGallery><images><image><filename>{filename}</filename></image></images></MibreitGallery>"
        gallery_element=parse_gallery_xml(test_xml)
        self.assertIsNotNone(gallery_element)
        self.assertEqual(get_image_element_filenames_list(
            gallery_element), [filename]) # type: ignore


class TestCreateImageElement(unittest.TestCase):

    def test_create_size_1(self):
        new_xml_image_element=create_image_element(
            "test_image", "test_caption", "test_alt", "test_altde", "1")
        self.assertEqual(XmlEt.tostring(new_xml_image_element, encoding="unicode"), '''<image>
<filename>test_image</filename>
<caption>test_caption</caption>
<alt>test_alt</alt>
<altDe>test_altde</altDe>
<prints size="small" />
</image>''')

    def test_create_size_2(self):
        new_xml_image_element=create_image_element(
            "test_image", "test_caption", "test_alt", "test_altde", "2")
        self.assertEqual(XmlEt.tostring(new_xml_image_element, encoding="unicode"), '''<image>
<filename>test_image</filename>
<caption>test_caption</caption>
<alt>test_alt</alt>
<altDe>test_altde</altDe>
<prints size="medium" />
</image>''')

    def test_create_size_3(self):
        new_xml_image_element=create_image_element(
            "test_image", "test_caption", "test_alt", "test_altde", "3")
        self.assertEqual(XmlEt.tostring(new_xml_image_element, encoding="unicode"), '''<image>
<filename>test_image</filename>
<caption>test_caption</caption>
<alt>test_alt</alt>
<altDe>test_altde</altDe>
<prints size="large" />
</image>''')


class TestUpdateImageDescriptions(unittest.TestCase):
    __input_side_effects=['title', 'english', 'german']

    @ patch('builtins.input', side_effect=__input_side_effects)
    def test_update_image_descriptions(self, mock_input):
        images_element=XmlEt.fromstring(
            f"""<images><image><filename>fname</filename></image></images>""")
        update_image_descriptions(images_element)
        self.assertEqual(XmlEt.tostring(images_element, encoding="unicode"),
                         f"<images><image><filename>fname</filename><caption>{self.__input_side_effects[0]}</caption><alt>{self.__input_side_effects[1]}</alt><altDe>{self.__input_side_effects[2]}</altDe></image></images>")

    @ patch('builtins.input', side_effect=__input_side_effects)
    def test_update_image_descriptions_callback(self, mock_input):
        image_element=XmlEt.fromstring(
            f"""<images><image><filename>fname</filename></image></images>""")
        new_image_description=None
        new_image_title=None

        def callback(image_name, image_title, image_description):
            nonlocal new_image_description, new_image_title
            new_image_description=image_description
            new_image_title=image_title

        update_image_descriptions(image_element, callback)

        self.assertEqual(new_image_title, self.__input_side_effects[0])
        self.assertEqual(new_image_description, self.__input_side_effects[1])


if __name__ == '__main__':
    unittest.main()
