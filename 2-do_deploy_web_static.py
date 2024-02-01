#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers using the function do_deploy.
"""

from fabric.api import env, put, run
from os.path import exists
from datetime import datetime
import os

# Set the environment variables
env.user = 'ubuntu'  # Update with your username
env.hosts = ['<IP web-01>', '<IP web-02>']  # Update with your server IPs

def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path: Path to the archive to be deployed.

    Returns:
        True if all operations are done correctly, False otherwise.
    """
    if not exists(archive_path):
        return False

    # Get the filename without extension
    filename = os.path.basename(archive_path)
    filename_no_ext = os.path.splitext(filename)[0]

    # Upload the archive to /tmp/ directory on the web server
    put(archive_path, "/tmp/{}".format(filename))

    # Create the release directory
    run("mkdir -p /data/web_static/releases/{}/".format(filename_no_ext))

    # Uncompress the archive to the release directory
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(filename, filename_no_ext))

    # Remove the uploaded archive
    run("rm /tmp/{}".format(filename))

    # Move the contents to the proper location
    run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(filename_no_ext, filename_no_ext))

    # Remove the empty web_static directory
    run("rm -rf /data/web_static/releases/{}/web_static".format(filename_no_ext))

    # Remove the current symbolic link
    run("rm -rf /data/web_static/current")

    # Create a new symbolic link to the new version
    run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(filename_no_ext))

    print("New version deployed!")

    return True
