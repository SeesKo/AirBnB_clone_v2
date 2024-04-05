#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import *
import os

env.hosts = ['100.25.15.192', '3.94.181.137']


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_name)[0]
        remote_path = "/tmp/{}".format(archive_name)
        releases_path = "/data/web_static/releases/"
        current_path = "/data/web_static/current"

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, remote_path)

        # Uncompress the archive to folder
        run("mkdir -p {}/{}".format(releases_path, archive_no_ext))
        run("tar -xzf {} -C {}/{}".format(
            remote_path, releases_path, archive_no_ext))

        # Delete the archive from the web server
        run("rm {}".format(remote_path))

        # Move files to proper location
        run("mv {}/{}/web_static/* {}/{}".format(
            releases_path, archive_no_ext, releases_path, archive_no_ext))
        run("rm -rf {}/web_static".format(releases_path, archive_no_ext))

        # Delete the symbolic link from the web server
        run("rm -rf {}".format(current_path))

        # Create a new the symbolic link on the web server
        run("ln -s {}/{} {}".format(
            releases_path, archive_no_ext, current_path))

        return True
    except Exception:
        return False
