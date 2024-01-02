import unittest
from unittest.mock import patch, MagicMock
from modules.gallery_tools import is_gallery_path, get_list_of_supported_images_in_folder
from modules.gallery_configuration import GALLERY_FOLDER_SMALL, GALLERY_FOLDER_IMAGES, GALLERY_FILE_GALLERY, REQUIRED_GALLERY_ELEMENTS

gallery_folder = "gallery_folder"
no_gallery_folder_small_missing = "no_gallery_folder_small_missing"
no_gallery_folder_images_missing = "no_gallery_folder_images_missing"
no_gallery_folder_file_gallery_missing = "no_gallery_folder_file_gallery_missing"
images_folder = "images_folder"
valid_images = ["img1.jpg", "img2.jpeg"]
images = valid_images+["img3.png"]


def mock_listdir(folder):
    if (folder == gallery_folder):
        return [GALLERY_FOLDER_SMALL, GALLERY_FOLDER_IMAGES, GALLERY_FILE_GALLERY]
    elif (folder == no_gallery_folder_small_missing):
        return [GALLERY_FOLDER_IMAGES, GALLERY_FILE_GALLERY]
    elif (folder == no_gallery_folder_images_missing):
        return [GALLERY_FOLDER_SMALL, GALLERY_FILE_GALLERY]
    elif (folder == no_gallery_folder_file_gallery_missing):
        return [GALLERY_FOLDER_IMAGES, GALLERY_FOLDER_SMALL]
    else:  # images_folder
        return images


@patch('modules.gallery_tools.listdir', mock_listdir)
class TestGalleryImageElement(unittest.TestCase):

    def test_is_gallery_path(self):
        self.assertEqual(is_gallery_path(gallery_folder), True)

    def test_is_gallery_path_images_missing(self):
        self.assertEqual(is_gallery_path(
            no_gallery_folder_images_missing), False)

    def test_is_gallery_path_gallery_missing(self):
        self.assertEqual(is_gallery_path(
            no_gallery_folder_file_gallery_missing), False)

    def test_get_list_of_supported_images_in_folder_returns_only_jpg(self):
        self.assertEqual(get_list_of_supported_images_in_folder(
            images_folder), valid_images)


if __name__ == '__main__':
    unittest.main()
