from os import path
import subprocess
import platform
import json

tags_to_keep = ["SourceFile", "ExifToolVersion", "Copyright", "Rights", "Creator", "CreatorCountry",
                "CreatorWorkEmail", "CreatorWorkURL", "UsageTerms", "CopyrightNotice", "Description", "ImageDescription", "Title"]

groups_to_keep = ["SourceFile", "ExifTool",
                  "File", "ICC_Profile", "Composite", "APP14"]


class GalleryExifUpdate:
    __exif_tool_executable = None

    def __init__(self):
        platform_name = platform.system()

        if platform_name == 'Windows':
            self.__exif_tool_executable = "exiftool.exe"
        else:
            self.__exif_tool_executable = "./exiftool"

    def __get_tags_to_remove(self, exif_data):
        tags_to_remove = []
        for group_tag, group_value in exif_data.items():
            if group_tag in groups_to_keep:
                pass
            elif isinstance(group_value, dict):
                for k, v in group_value.items():
                    if k not in tags_to_keep:
                        tags_to_remove.append(k)
            elif isinstance(group_value, str):
                if group_tag not in tags_to_keep:
                    tags_to_remove.append(group_tag)
        return tags_to_remove

    def update(self, images_folder: str, image_name: str, caption: str, description: str):
        image_path = path.join(images_folder, image_name)
        if path.exists(self.__exif_tool_executable) and path.exists(image_path):
            exif_tool_execute = [self.__exif_tool_executable]
            exif_tool_execute.append("-overwrite_original")
            exif_tool_execute.append(f"-ImageDescription={description}")
            exif_tool_execute.append(f"-Description={description}")
            exif_tool_execute.append(f"-Title={caption}")

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
