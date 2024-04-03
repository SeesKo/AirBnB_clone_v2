#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""
from fabric.api import env, local
from datetime import datetime
from os.path import exists
from os import path

env.hosts = ['100.25.15.192', '3.94.181.137']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        if not path.exists('versions'):
            local('mkdir versions')
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = 'versions/web_static_{}.tgz'.format(timestamp)
        local('tar -czvf {} web_static'.format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers and deploys it
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract archive to folder
        filename = path.basename(archive_path)
        folder_name = "/data/web_static/releases/{}".format(filename[:-4])
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_name))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current linked to the new version
        run("ln -s {} /data/web_static/current".format(folder_name))

        return True
    except Exception as e:
        return False


def deploy():
    """
    Creates and distributes an archive to your web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
