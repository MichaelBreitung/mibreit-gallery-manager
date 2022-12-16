# mibreit-gallery-manager

This set of Python scripts is intended to be used together with the [mibreit-homepage-template](https://github.com/MichaelBreitung/mibreit-homepage-template). 

Adding and removing images from the image galleries within a homepage created with this template typically requires manual editing of XML files. Using the Python script this process is much simpler.

## Requirements

Python (Version 3.11) must be installed on system. Then you can use *pip install -r requirements.txt* to install the required packages. 

## Usage

Call *python gallery_manager.py -i **path to galleries*** for the script to traverse all contained gallery folders and prompt you for new images that have been added or for images that have been removed.