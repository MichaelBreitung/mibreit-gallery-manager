# global constants
REQUIRED_GALLERY_FOLDER_IMAGES = "images"
REQUIRED_GALLERY_FOLDER_SMALL = "small"
REQUIRED_GALLERY_FILE_GALLERY = "gallery.xml"
REQUIRED_GALLERY_ELEMENTS = {REQUIRED_GALLERY_FILE_GALLERY,
                             REQUIRED_GALLERY_FOLDER_IMAGES, REQUIRED_GALLERY_FOLDER_SMALL}

GALLERY_XML_IMAGES_TAG = "images"
GALLERY_XML_IMAGES_FILENAME_TAG = "filename"
GALLERY_XML_IMAGES_CAPTION_TAG = "caption"
GALLERY_XML_IMAGES_ALT_TAG = "alt"
GALLERY_XML_IMAGES_ALTDE_TAG = "altDe"
GALLERY_XML_IMAGES_PRINTS_TAG = "prints"

CONFIG_CREATOR_NAME = "creator_name"
CONFIG_CREATOR_URL = "creator_url"
CONFIG_CREATOR_EMAIL = "creator_email"
CONFIG_COPYRIGHT = "copyright_notice"
CONFIG_WEB_STATEMENT = "web_statement"
CONFIG_LICENSOR_NAME = "licensor_name"
CONFIG_LICENSOR_URL = "licensor_url"
CONFIG_LICENSOR_EMAIL = "licensor_email"
CONFIG_CREDIT = "credit"
CONFIG_CREDIT_SHORT = "credit_short"
CONFIG_USAGE_TERMS = "usage_terms"

IMAGE_METADATA_GROUPS_TO_KEEP = ["SourceFile", "ExifTool",
                                 "File", "ICC_Profile", "Composite", "APP14"]

IMAGE_METADATA_TAGS_TO_KEEP = ["SourceFile", "ExifToolVersion",
                               "Title", "Description", "ImageDescription"]

CONFIG_EXIF_MAPPING = {
    CONFIG_CREATOR_NAME: ["Creator", "ImageCreatorName", "CopyrightOwnerName"],
    CONFIG_CREATOR_URL: "CreatorWorkURL",
    CONFIG_CREATOR_EMAIL: "CreatorWorkEmail",
    CONFIG_COPYRIGHT: ["Copyright", "CopyrightNotice", "Rights"],
    CONFIG_CREDIT: "XMP:Credit",
    CONFIG_CREDIT_SHORT: "IPTC:Credit",
    CONFIG_USAGE_TERMS: "UsageTerms",
    CONFIG_LICENSOR_URL: "LicensorURL",
    CONFIG_LICENSOR_EMAIL: "LicensorEmail",
    CONFIG_LICENSOR_NAME: "LicensorName",
    CONFIG_WEB_STATEMENT: "WebStatement"
}


def remove_group_from_tag(tag: str) -> str:
    group_end = tag.rfind(":")
    if group_end != -1:
        return tag[(group_end+1):]
    return tag


for k, v in CONFIG_EXIF_MAPPING.items():
    if isinstance(v, list):
        for element in v:
            IMAGE_METADATA_TAGS_TO_KEEP.append(remove_group_from_tag(element))
    else:
        IMAGE_METADATA_TAGS_TO_KEEP.append(remove_group_from_tag(v))

THUMBNAIL_SIZE = (200, 200)
THUMB_SHARPEN_FACTOR = 1.5
THUMB_QUALITY = 70
