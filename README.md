# mibreit-gallery-manager

This set of Python scripts is intended to be used together with the [mibreit-homepage-template](https://github.com/MichaelBreitung/mibreit-homepage-template). 

Adding and removing images from the image galleries within a homepage created with this template typically requires manual editing of XML files. Using the Python script this process is much simpler.

## Prerequisites

This project uses a Dev Container to provide the required tools and dependencies for Python development. You must have VS Code and the Dev Containers extension installed on your host machine as well as the Docker Engine. On Windows, you can use Docker Desktop, for example. To avoid problems with the mounting of ssh keys, it is recommended, though, to use WSL2 with a Ubuntu distribution and install Docker there.

Here are three video tutorials that will get you started with Docker and Dev Containers:
- [Where Dev Containers are helpful](https://youtu.be/9F-jbT-pHkg?si=yW4RThXZNC0SMIyl)
- [How to create a custom Dev Container](https://youtu.be/7P0pTECkiN8?si=51YPKbUzL7OlAs80)
- [How to configure VS Code Extenstions and Settings in a Dev Container](https://youtu.be/W84R1CxtF0c?si=YBhBRzKk1lgCKEyz)

You also need to download the latest version of Phil Harvey's ExifTool. It is used via *subprocess* and needs to be either available in the *path* or in the root of this project.

## Usage

Call ``python3 gallery_manager.py -i **path to galleries**`` for the script to traverse all contained gallery folders and prompt you for new images that have been added or for images that have been removed.

## Unit Testing

This package includes unit tests. The following commands will be helpful:

- runs the unit tests 
``python3 -m unittest``

- tests the coverage of the unit tests
``python3 -m coverage run -m unittest``

- called after the previous command, it creates a report showing the coverage
``python3 -m coverage report``
