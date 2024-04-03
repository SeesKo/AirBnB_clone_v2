#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""
from fabric.api import env, run
from datetime import datetime
from os.path import exists
from os import makedirs
from fabric.operations import put
from fabric.contrib import files
from fabric.contrib.files import exists

env.hosts = ['100.25.15.192', '3.94.181.137']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(timestamp)

        if not exists("versions"):
            makedirs("versions")

        local("tar -cvzf {} web_static".format(file_name))

        return file_name
    except OSError as e:
        print("Error: {}".format(e))
        return None
    except Exception as e:
        print("Error: {}".format(e))
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[1]

        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/".format(archive_name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_name, archive_name))
        run("rm /tmp/{}".format(archive_name))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/"
            .format(archive_name, archive_name))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_name))
        return True
    except Exception as e:
        print("Error: {}".format(e))
        return False


def deploy():
    """
    Call the do_pack() function and store the path of the created archive
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
