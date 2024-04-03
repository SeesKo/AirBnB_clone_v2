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
    try:
        number = int(number)
        if number < 0:
            number = 0

        versions_path = "/data/web_static/releases/"
        archives_path = "versions/"

        with lcd(archives_path):
            local_archives = [f for f in listdir(".") if isfile(join(".", f))]

        local_archives.sort(reverse=True)

        if number == 0:
            number = 1

        archives_to_keep = local_archives[:number]

        with cd(versions_path):
            remote_archives = run("ls -1t | grep -E '^web_static_.*.tgz$'").split('\n')

        remote_archives.sort(reverse=True)

        if number == 0:
            number = 1

        remote_archives_to_keep = remote_archives[:number]

        for archive in local_archives:
            if archive not in archives_to_keep:
                local("rm -f {}".format(archive))

        for archive in remote_archives:
            if archive not in remote_archives_to_keep:
                run("rm -f {}".format(archive))

    except Exception as e:
        print("Error: {}".format(e))
        return False

    return True


if __name__ == "__main__":
    import sys
    do_clean(*sys.argv[1:])
