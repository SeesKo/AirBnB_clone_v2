#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import env, put, run
from datetime import datetime
import os


# Define the servers
env.hosts = ['100.25.15.192', '3.94.181.137']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers and deploys it
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract archive to folder
        filename = os.path.basename(archive_path)
        folder_name = "/data/web_static/releases/{}".format(filename[:-4])
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_name))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link linked to the new version
        run("ln -s {} /data/web_static/current".format(folder_name))

        return True
    except Exception as e:
        return False
