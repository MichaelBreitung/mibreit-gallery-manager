import re
from shutil import copy
from os import mkdir, path

allowedCharacters = re.compile(r'[a-zA-Z-]*$')

class GalleryCreator:
    def __init__(self, __galleries_path: str):
        self.__galleries_path = __galleries_path

    def create(self):
        gallery_name = input(
                "-> Please provide a gallery name - use only regular lower and upper-case characters and '-': ")
        if allowedCharacters.match(gallery_name):
            if not path.isdir(gallery_name):
                full_gallery_path = path.join(self.__galleries_path, gallery_name)
                script_path = path.join(path.dirname(path.abspath(__file__)), "..")
                mkdir(full_gallery_path)
                mkdir(f"{full_gallery_path}/images")
                mkdir(f"{full_gallery_path}/small")
                copy(f"{script_path}/templates/gallery.xml", f"{full_gallery_path}/")
                copy(f"{script_path}/templates/replaceme.jpg", f"{full_gallery_path}/images")
            else:
                print(f"-> {gallery_name} folder already exists")
        else:
            print(f"-> only characters and - allowed in {gallery_name}")
        