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

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
