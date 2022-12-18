import unittest
from modules.gallery_image_element import *
import xml.etree.ElementTree as XmlEt


class TestGalleryImageElement(unittest.TestCase):

    def test_create_size_1(self):
        new_xml_image_element = GalleryImageElement(
            "test_image", "test_caption", "test_alt", "test_altde", "1").create()
        self.assertEqual(XmlEt.tostring(new_xml_image_element, encoding="unicode"), '''<image>
<filename>test_image</filename>
<caption>test_caption</caption>
<alt>test_alt</alt>
<altDe>test_altde</altDe>
<prints size="small" />
</image>''')

    def test_create_size_2(self):
        new_xml_image_element = GalleryImageElement(
            "test_image", "test_caption", "test_alt", "test_altde", "2").create()
        self.assertEqual(XmlEt.tostring(new_xml_image_element, encoding="unicode"), '''<image>
<filename>test_image</filename>
<caption>test_caption</caption>
<alt>test_alt</alt>
<altDe>test_altde</altDe>
<prints size="medium" />
</image>''')

    def test_create_size_3(self):
        new_xml_image_element = GalleryImageElement(
            "test_image", "test_caption", "test_alt", "test_altde", "3").create()
        self.assertEqual(XmlEt.tostring(new_xml_image_element, encoding="unicode"), '''<image>
<filename>test_image</filename>
<caption>test_caption</caption>
<alt>test_alt</alt>
<altDe>test_altde</altDe>
<prints size="large" />
</image>''')


if __name__ == '__main__':
    unittest.main()
