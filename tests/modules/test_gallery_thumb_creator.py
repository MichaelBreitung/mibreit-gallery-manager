import unittest
from unittest.mock import patch, MagicMock
from os import path
from modules.gallery_thumb_creator import *
from modules.gallery_configuration import THUMB_QUALITY, THUMB_SHARPEN_FACTOR, THUMBNAIL_SIZE


class TestGalleryThumbCreator(unittest.TestCase):
    __images_path = "some/images/path"
    __thumbs_path = "some/thumbs/path"
    __thumb_name = "thumbName.jpg"

    def __mock_image_image_class(self, mock_image, mock_image_enhance):
        mock_image_object = MagicMock()
        mock_image_object.copy.return_value = mock_image_object
        mock_image_object.enhance.return_value = mock_image_object
        mock_image_enhance.Sharpness.return_value = mock_image_object
        mock_image.open.return_value = mock_image_object
        return mock_image_object

    @patch('modules.gallery_thumb_creator.Image')
    @patch('modules.gallery_thumb_creator.ImageEnhance')
    def test_create_thumb(self, mock_image_enhance, mock_image):
        mock_image_object = self.__mock_image_image_class(mock_image, mock_image_enhance)

        creator = GalleryThumbCreator(self.__images_path, self.__thumbs_path)
        creator.create(self.__thumb_name)

        mock_image.open.assert_called_once_with(path.join(
            self.__images_path, self.__thumb_name))
        mock_image_object.copy.assert_called_once()
        mock_image_object.thumbnail.assert_called_once_with(
            THUMBNAIL_SIZE, mock_image.LANCZOS)
        mock_image_object.enhance.assert_called_once_with(
            THUMB_SHARPEN_FACTOR)
        mock_image_object.save.assert_called_once_with(path.join(
            self.__thumbs_path, self.__thumb_name), quality=THUMB_QUALITY)


if __name__ == '__main__':
    unittest.main()
