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
        self.assertEqual(XmlEt.tostring(parse_gallery_xml(
            test_xml), encoding="unicode"), test_xml)

    def test_get_images_element_succeeds_for_empty_element(self):
        test_xml = "<MibreitGallery><images /></MibreitGallery>"
        gallery_element = parse_gallery_xml(test_xml)
        self.assertEqual(XmlEt.tostring(get_images_element(
            gallery_element), encoding="unicode"), "<images />")

    def test_get_images_element_succeeds_for_list(self):
        test_xml = "<MibreitGallery><images><image/></images></MibreitGallery>"
        gallery_element = parse_gallery_xml(test_xml)
        self.assertEqual(XmlEt.tostring(get_images_element(
            gallery_element), encoding="unicode"), "<images><image /></images>")

    def test_extract_filename_from_empty_image_element(self):
        test_xml = "<image></image>"
        image_element = XmlEt.fromstring(test_xml)
        self.assertEqual(
            extract_filename_from_image_element(image_element), None)

    def test_extract_filename_from_image_element(self):
        filename = "test"
        test_xml = f"<image><filename>{filename}</filename></image>"
        image_element = XmlEt.fromstring(test_xml)
        self.assertEqual(
            extract_filename_from_image_element(image_element), filename)

    def test_get_image_element_filenames_for_empty_element(self):
        test_xml = "<MibreitGallery><images /></MibreitGallery>"
        gallery_element = parse_gallery_xml(test_xml)
        self.assertEqual(get_image_element_filenames_list(
            gallery_element), [])

    def test_get_image_element_filenames_for_element_without_filename(self):
        test_xml = "<MibreitGallery><images><image /></images></MibreitGallery>"
        gallery_element = parse_gallery_xml(test_xml)
        self.assertEqual(get_image_element_filenames_list(
            gallery_element), [])

    def test_get_image_element_filenames_for_element_with_empty_filename(self):
        test_xml = "<MibreitGallery><images><image><filename></filename></image></images></MibreitGallery>"
        gallery_element = parse_gallery_xml(test_xml)
        self.assertEqual(get_image_element_filenames_list(
            gallery_element), [])

    def test_get_image_element_filenames_for_element_with_filename(self):
        filename = "test"
        test_xml = f"<MibreitGallery><images><image><filename>{filename}</filename></image></images></MibreitGallery>"
        gallery_element = parse_gallery_xml(test_xml)
        self.assertEqual(get_image_element_filenames_list(
            gallery_element), [filename])


class TestCreateImageElement(unittest.TestCase):

    def test_create_size_1(self):
        new_xml_image_element = create_image_element(
            "test_image", "test_caption", "test_alt", "test_altde", "1")
        self.assertEqual(XmlEt.tostring(new_xml_image_element, encoding="unicode"), '''<image>
<filename>test_image</filename>
<caption>test_caption</caption>
<alt>test_alt</alt>
<altDe>test_altde</altDe>
<prints size="small" />
</image>''')

    def test_create_size_2(self):
        new_xml_image_element = create_image_element(
            "test_image", "test_caption", "test_alt", "test_altde", "2")
        self.assertEqual(XmlEt.tostring(new_xml_image_element, encoding="unicode"), '''<image>
<filename>test_image</filename>
<caption>test_caption</caption>
<alt>test_alt</alt>
<altDe>test_altde</altDe>
<prints size="medium" />
</image>''')

    def test_create_size_3(self):
        new_xml_image_element = create_image_element(
            "test_image", "test_caption", "test_alt", "test_altde", "3")
        self.assertEqual(XmlEt.tostring(new_xml_image_element, encoding="unicode"), '''<image>
<filename>test_image</filename>
<caption>test_caption</caption>
<alt>test_alt</alt>
<altDe>test_altde</altDe>
<prints size="large" />
</image>''')


class TestUpdateImageDescriptions(unittest.TestCase):
    __input_side_effects = ['english', 'german']

    @patch('builtins.input', side_effect=__input_side_effects)
    def test_update_image_descriptions(self, mock_input):
        image_element = XmlEt.fromstring(
            f"""<images><image></image></images>""")
        update_image_descriptions(image_element)
        self.assertEqual(XmlEt.tostring(image_element, encoding="unicode"),
                         f"<images><image><alt>{self.__input_side_effects[0]}</alt><altDe>{self.__input_side_effects[1]}</altDe></image></images>")

    @patch('builtins.input', side_effect=__input_side_effects)
    def test_update_image_descriptions_callback(self, mock_input):
        image_element = XmlEt.fromstring(
            f"""<images><image></image></images>""")
        new_image_description = None

        def callback(image_name, image_description):
            nonlocal new_image_description
            new_image_description = image_description

        update_image_descriptions(image_element, callback)

        self.assertEqual(new_image_description, self.__input_side_effects[0])


if __name__ == '__main__':
    unittest.main()
