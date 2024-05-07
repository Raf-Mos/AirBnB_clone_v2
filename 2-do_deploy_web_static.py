#!/usr/bin/python3
"""
Fabfile to server
"""
from fabric.api import local, env, put, run
from os.path import isfile

env.hosts = ["54.87.106.95", "100.25.10.97"]


def do_pack():
    """ Generates a .tgz archive from web_static folder."""
    local("mkdir -p versions")
    timestamp = local("date '+%Y%m%d%H%M%S'", capture=True)
    archive_path = "versions/web_static_{}.tgz".format(timestamp)
    result = local("tar -czvf {} web_static".format(archive_path))
    return archive_path if isfile(archive_path) else None


def do_deploy(archive_path):
    """ Distributes an archive to the web servers. """
    if not isfile(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        archive_no_ext = archive_name.split(".")[0]

        put(archive_path, "/tmp/{}".format(archive_name))
        run("mkdir -p /data/web_static/releases/{}/".format(archive_no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_name, archive_no_ext))
        run("rm /tmp/{}".format(archive_name))
        run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/"
            .format(archive_no_ext, archive_no_ext))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_no_ext))
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False


def deploy():
    """ Deploys an archive to the web servers. """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
