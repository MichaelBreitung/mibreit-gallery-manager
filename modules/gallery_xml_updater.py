from os import path, remove
from .gallery_tools import get_list_of_supported_images_in_folder
from .gallery_xml_tools import extract_filename_from_image_element, read_gallery_xml, parse_gallery_xml, \
    print_images_list, create_image_element, write_formatted_xml, get_image_element_filenames_list, get_images_element
from .gallery_configuration import REQUIRED_GALLERY_FILE_GALLERY, \
    REQUIRED_GALLERY_FOLDER_IMAGES


class GalleryXmlUpdater:
    __images_path = None
    __images_set = None
    __gallery_path = None
    __xml_gallery_tree = None

    def __init__(self, images_path, gallery_path):
        self.__images_path = images_path
        self.__gallery_path = gallery_path
        self.__images_set = self.__images_set = set(get_list_of_supported_images_in_folder(
            images_path))

    def __remove_images_from_gallery(self, superfluous_gallery_elements: set[str]):
        images_element = get_images_element(self.__xml_gallery_tree)
        xml_image_elements_to_remove = []

        for image_element in images_element:
            image_name = extract_filename_from_image_element(image_element)
            if image_name in superfluous_gallery_elements:
                print(f"\n{image_name}:")
                response = input(
                    f"-> Image is present in {REQUIRED_GALLERY_FILE_GALLERY}, but not in {REQUIRED_GALLERY_FOLDER_IMAGES}. Shall it be removed from {REQUIRED_GALLERY_FILE_GALLERY}? (yes/no) ")
                if response in ("yes", "y"):
                    print(
                        f"-> Removing image {image_name} from {REQUIRED_GALLERY_FILE_GALLERY}")
                    xml_image_elements_to_remove.append(image_element)

        for image_element in xml_image_elements_to_remove:
            images_element.remove(image_element)

    def __add_images_to_gallery(self, missing_gallery_elements):
        images_element = get_images_element(self.__xml_gallery_tree)

        for image_name in missing_gallery_elements:
            print(f"\n{image_name}:")
            response = input(
                f"-> Image is present in {REQUIRED_GALLERY_FOLDER_IMAGES}, but not in {REQUIRED_GALLERY_FILE_GALLERY}. Shall it be removed from {REQUIRED_GALLERY_FOLDER_IMAGES}? (yes/no) ")
            if response in ("yes", "y"):
                print(
                    f"-> Removing image {image_name} from {REQUIRED_GALLERY_FOLDER_IMAGES}")
                remove(path.join(self.__images_path, image_name))
            else:
                response = input(
                    f"-> Shall it instead be created inside {REQUIRED_GALLERY_FILE_GALLERY}? (yes/no) ")
                if response in ("yes", "y"):
                    caption = input(f"-> Please provide a caption: ")
                    alt = input(f"-> Please provide a description: ")
                    altGer = input(f"-> Please provide a german description: ")
                    size = input(
                        f"-> Please provide a maximum print size (1 - up to 45cm; 2 - up to 60cm; 3 - up to 90cm): ")

                    print_images_list(self.__xml_gallery_tree)
                    index = int(
                        input(f"-> At which index shall the image be inserted? "))
                    new_xml_image_element = create_image_element(
                        image_name, caption, alt, altGer, size)
                    images_element.insert(index, new_xml_image_element)

    def update(self):
        xml_data = read_gallery_xml(self.__gallery_path)
        self.__xml_gallery_tree = parse_gallery_xml(xml_data)

        if self.__xml_gallery_tree != None:
            images_in_gallery_set = set(
                get_image_element_filenames_list(self.__xml_gallery_tree))

            self.__remove_images_from_gallery(
                images_in_gallery_set - self.__images_set)

            self.__add_images_to_gallery(
                self.__images_set - images_in_gallery_set)

            write_formatted_xml(self.__xml_gallery_tree, self.__gallery_path)
            return True
        else:
            return False
