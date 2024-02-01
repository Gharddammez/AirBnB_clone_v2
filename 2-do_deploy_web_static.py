#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers using the function do_deploy.
"""

from fabric.api import env, put, run
from os.path import exists
import os

# Set the environment variables
env.user = 'ubuntu'  # Update with your username
env.hosts = ['<34.232.52.252>', '<18.233.64.118>']  # Update with your server IPs

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
    put(archive_path, f"/tmp/{filename}")

    # Create the release directory
    run(f"mkdir -p /data/web_static/releases/{filename_no_ext}/")

    # Uncompress the archive to the release directory
    run(f"tar -xzf /tmp/{filename} -C /data/web_static/releases/{filename_no_ext}/")

    # Remove the uploaded archive
    run(f"rm /tmp/{filename}")

    # Move the contents to the proper location
    run(f"mv /data/web_static/releases/{filename_no_ext}/web_static/* /data/web_static/releases/{filename_no_ext}/")

    # Remove the empty web_static directory
    run(f"rm -rf /data/web_static/releases/{filename_no_ext}/web_static")

    # Remove the current symbolic link
    run(f"rm -rf /data/web_static/current")

    # Create a new symbolic link to the new version
    run(f"ln -s /data/web_static/releases/{filename_no_ext}/ /data/web_static/current")

    print("New version deployed!")

    return True
