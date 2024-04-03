#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import *
from os.path import exists

# Define the servers
env.hosts = ['100.25.15.192', '3.94.181.137']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers and deploys it
    """
    if exists(archive_path):
        print(archive_path)
        put(archive_path, '/tmp/')
        file_name = archive_path.split('/')[-1]
        folder_name = file_name.replace('.tgz', '')
        print(folder_name)
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(
            file_name,
            folder_name
        ))
        run('rm /tmp/{}'.format(file_name))
        run('mv {}/{}/web_static/* /data/web_static/releases/{}'.format(
            '/data/web_static/releases',
            folder_name,
            folder_name
            ))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(
            folder_name
            ))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/{}/ /data/web_static/current'.format(
            '/data/web_static/releases',
            folder_name
            ))
        return True
    else:
        return False
