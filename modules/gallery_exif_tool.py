from os import path
import subprocess
import platform
import json
from .gallery_configuration import CONFIG_EXIF_MAPPING, IMAGE_METADATA_GROUPS_TO_KEEP, IMAGE_METADATA_TAGS_TO_KEEP


def read_configuration(config_path: str) -> dict[str, str] | None:
    with open(config_path) as file:
        data = json.load(file)
        if data.get("exif") is not None:
            return data["exif"]

    return None


class GalleryExifUpdate:
    __exif_tool_executable: str = "./exiftool"
    __exif_tool_params_from_settings: list[str] = []

    def __init__(self, settings: dict[str, str] | None = None):
        platform_name = platform.system()

        if platform_name == 'Windows':
            self.__exif_tool_executable = "exiftool.exe"
            if path.exists("exiftool.exe"):
                self.__has_executable = True
        else:
            if path.exists("exiftool"):
                self.__has_executable = True

        if settings is not None:
            for k, v in CONFIG_EXIF_MAPPING.items():
                if settings.get(k) is not None:
                    if isinstance(v, list):
                        for element in v:
                            self.__exif_tool_params_from_settings.append(
                                f"-{element}={settings[k]}")
                    else:
                        self.__exif_tool_params_from_settings.append(
                            f"-{v}={settings[k]}")

    def __get_tags_to_remove(self, exif_data: dict[str, str]):
        remove = []
        for group_tag, group_value in exif_data.items():
            if group_tag in IMAGE_METADATA_GROUPS_TO_KEEP:
                pass
            elif isinstance(group_value, dict):
                for k, v in group_value.items():
                    if k not in IMAGE_METADATA_TAGS_TO_KEEP:
                        remove.append(k)
            elif isinstance(group_value, str):
                if group_tag not in IMAGE_METADATA_TAGS_TO_KEEP:
                    remove.append(group_tag)
        return remove

    def update(self, images_folder: str, image_name: str, caption: str, description: str):
        image_path = path.join(images_folder, image_name)
        if self.__has_executable and path.exists(image_path):
            exif_tool_execute = [self.__exif_tool_executable]
            exif_tool_execute.append("-overwrite_original")
            exif_tool_execute.append(f"-ImageDescription={description}")
            exif_tool_execute.append(f"-Description={description}")
            exif_tool_execute.append(f"-Title={caption}")
            exif_tool_execute.extend(self.__exif_tool_params_from_settings)

            # TODO: instad of multiple blocking run calls, keep process open use stdin and stdout
            # to control it
            return_value = subprocess.run(
                [self.__exif_tool_executable, "-j", "-groupHeadings", image_path], capture_output=True)
            exif_data = json.loads(return_value.stdout.decode())
            tags_to_remove = self.__get_tags_to_remove(exif_data[0])
            if len(tags_to_remove):
                exif_tool_execute.extend(
                    [f"-{tag}=" for tag in tags_to_remove])

            exif_tool_execute.append(image_path)
            subprocess.run(exif_tool_execute)
