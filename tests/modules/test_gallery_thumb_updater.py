import unittest
from unittest.mock import patch, MagicMock, call
from os import path
from modules.gallery_variants_updater import GalleryVariantsUpdater

images_path = path.normpath("some/images/path")
thumbs_path = path.normpath("some/thumbs/path")
empty_path = ""
img1 = "img1"
img2 = "img2"
img3 = "img3"
images = [img1, img2]
thumbs = [img1, img3]


def mock_get_list_of_supported_images_in_folder(folder):
    if folder == images_path:
        return images
    elif folder == thumbs_path:
        return thumbs
    else:  # empty_path
        return []


@patch("modules.gallery_variants_updater.GalleryThumbCreator")
@patch("modules.gallery_variants_updater.os.remove")
@patch("modules.gallery_variants_updater.os.makedirs")
@patch(
    "modules.gallery_variants_updater.get_list_of_supported_images_in_folder",
    mock_get_list_of_supported_images_in_folder,
)
class TestGalleryThumbCreator(unittest.TestCase):
    def test_update_thumbs_no_images(
        self, mock_makedirs, mock_remove, mock_thumb_creator
    ):
        mock_thumb_creator_object = MagicMock()
        mock_thumb_creator.return_value = mock_thumb_creator_object

        updater = GalleryVariantsUpdater(empty_path, thumbs_path)
        updater.update()

        mock_thumb_creator_object.create.assert_not_called()
        mock_remove.assert_has_calls(
            [call(path.join(thumbs_path, img1)), call(path.join(thumbs_path, img3))],
            any_order=True,
        )

        mock_makedirs.assert_called_once_with(thumbs_path, exist_ok=True)

    def test_update_thumbs_no_thumbs(
        self, mock_makedirs, mock_remove, mock_thumb_creator
    ):
        mock_thumb_creator_object = MagicMock()
        mock_thumb_creator.return_value = mock_thumb_creator_object

        updater = GalleryVariantsUpdater(images_path, empty_path)
        updater.update()

        mock_thumb_creator_object.create.assert_has_calls(
            [call(img1), call(img2)], any_order=True
        )
        mock_remove.assert_not_called()
        mock_makedirs.assert_called_once_with(empty_path, exist_ok=True)

    def test_update_thumbs_add_and_remove(
        self, mock_makedirs, mock_remove, mock_thumb_creator
    ):
        mock_thumb_creator_object = MagicMock()
        mock_thumb_creator.return_value = mock_thumb_creator_object

        updater = GalleryVariantsUpdater(images_path, thumbs_path)
        updater.update()

        mock_thumb_creator_object.create.assert_called_once_with(img2)
        mock_remove.assert_called_once_with(path.join(thumbs_path, img3))
        mock_makedirs.assert_called_once_with(thumbs_path, exist_ok=True)


if __name__ == "__main__":
    unittest.main()
