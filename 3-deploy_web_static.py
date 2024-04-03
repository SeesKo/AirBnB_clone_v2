#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""
from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['100.25.15.192', '3.94.181.137']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        filename = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(filename))
        return filename
    except Exception as ex:
        return None


def do_deploy(archive_path):
    """deploy web static with fabric"""
    if exists(archive_path) is False:
        return False

    try:
        filename = archive_path.split("/")[-1]
        no_excep = filename.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}{}/'.format(path, no_excep))
        run('sudo tar -xzf /tmp/{} -C {}{}/'.format(filename, path, no_excep))
        run('sudo rm /tmp/{}'.format(filename))
        run('sudo mv {0}{1}/web_static/* {0}{1}/'.format(path, no_excep))
        run('sudo rm -rf {}{}/web_static'.format(path, no_excep))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {}{}/ /data/web_static/current'.format(path, no_excep))
        return True
    except BaseException:
        return False


def deploy():
    """
    Call the do_pack() function and store the path of the created archive
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
