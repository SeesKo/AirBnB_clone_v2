#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives.
"""
from fabric.api import *
from datetime import datetime
import os

env.user = 'ubuntu'
env.hosts = ['100.25.15.192', '3.94.181.137']


def do_clean(number=0):
    """
    Deletes out-of-date archives from versions and folders.

    Args:
        number (int): Number of most recent archives to keep.
    """
    number = int(number)
    if number < 1:
        number = 1
    number += 1
    with lcd('versions'):
        local("ls -t | tail -n +{} | xargs -I {{}} rm -- {{}}"
        .format(number))
    with cd('/data/web_static/releases'):
        run("ls -t | tail -n +{} | xargs -I {{}} rm -rf -- {{}}"
        .format(number))
