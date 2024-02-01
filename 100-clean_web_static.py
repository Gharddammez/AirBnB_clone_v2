#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives, using the function do_clean.
"""

from fabric.api import env, local, run
from datetime import datetime
from os.path import exists

# Set the environment variables
env.user = 'ubuntu'
env.hosts = ['34.232.52.252', '18.233.64.118']  # Remove angle brackets and update with your server IPs


def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number: Number of archives, including the most recent, to keep.

    Returns:
        None
    """
    # Ensure the number is an integer
    number = int(number)

    # Local cleanup
    local("ls -lt versions | awk 'NR>{} {{print $NF}}' | xargs -I {{}} rm -f versions/{{}}".format(number))

    # Remote cleanup
    with cd('/data/web_static/releases/'):
        run("ls -lt | awk 'NR>{} {{print $NF}}' | xargs -I {{}} rm -rf {{}}".format(number))
