#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['100.25.15.192', '3.94.181.137']
env.user = 'ubuntu'


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    if int(number) < 2:
        number = 1
    else:
        number = int(number)

    local("cd versions; ls -t | tail -n +{} | xargs rm -f".format(number + 1))

    run("cd /data/web_static/releases; ls -t | tail -n +{} | xargs rm -rf".
        format(number + 1))
