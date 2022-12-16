import unittest
from modules.gallery_image_element import *
import xml.etree.ElementTree as XmlEt


class TestGalleryImageElement(unittest.TestCase):

    def test_create_size_1(self):
        new_xml_image_element = GalleryImageElement(
            "test_image", "test_caption", "1").create()
        self.assertEqual(XmlEt.tostring(new_xml_image_element, encoding="unicode"), '''<image>
<filename>test_image</filename>
<caption>test_caption</caption>
<prints size="small" />
</image>''')

    def test_create_size_2(self):
        new_xml_image_element = GalleryImageElement(
            "test_image", "test_caption", "2").create()
        self.assertEqual(XmlEt.tostring(new_xml_image_element, encoding="unicode"), '''<image>
<filename>test_image</filename>
<caption>test_caption</caption>
<prints size="medium" />
</image>''')

    def test_create_size_3(self):
        new_xml_image_element = GalleryImageElement(
            "test_image", "test_caption", "3").create()
        self.assertEqual(XmlEt.tostring(new_xml_image_element, encoding="unicode"), '''<image>
<filename>test_image</filename>
<caption>test_caption</caption>
<prints size="large" />
</image>''')


if __name__ == '__main__':
    unittest.main()
