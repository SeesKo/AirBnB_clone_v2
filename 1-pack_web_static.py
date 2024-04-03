#!/usr/bin/env python3
"""
Fabric script that generates a .tgz archive
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        # Create the folder versions if it doesn't exist
        local("mkdir -p versions")

        # Create the filename with the current date and time
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(timestamp)

        # Create the .tgz archive
        local("tar -cvzf {} web_static".format(file_name))

        # Return the archive path if the archive has been correctly generated
        return file_name
    except Exception:
        return None


if __name__ == "__main__":
    do_pack()
