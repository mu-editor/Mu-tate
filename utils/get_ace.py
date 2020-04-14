"""
Checks the latest release from the "Ace" project
(https://github.com/ajaxorg/ace-builds) which provides builds of the Ace code
editor.
"""
import click
import glob
import json
import logging
import os
import requests
import shutil
import tempfile
import zipfile


# Refers to the root of the project.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The log file (for all the details).
LOGFILE = os.path.join(BASE_DIR, "get_ace.log")
# Python directory.
ACE_DIR = os.path.join(BASE_DIR, "mu", "js", "ace")
# Version tag file (keeps track of tags of latest release).
TAG_FILE = os.path.join(BASE_DIR, "versions.json")


# Setup logging.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logfile_handler = logging.FileHandler(LOGFILE)
log_formatter = logging.Formatter("%(levelname)s: %(message)s")
logfile_handler.setFormatter(log_formatter)
logger.addHandler(logfile_handler)


def get_latest_tag():
    """
    Find the value of the latest tag for the stand-alone builds of Python.

    :return: The most recent tag value for the project.
    """
    url = "https://api.github.com/repos/ajaxorg/ace-builds/tags"
    logger.info("Requesting tag information: {}".format(url))
    response = requests.get(url)
    logger.info("Response url: {}".format(response.url))
    tag = response.json()[0]["name"]
    logger.info(f"Remote tag: {tag}")
    return tag


def download_file(url, tmpdir):
    """
    Download a build into the tmpdir.
    """
    click.echo(f"Downloading {url}")
    logger.info(f"Downloading {url}")
    r = requests.get(url, stream=True)
    if r.status_code != requests.codes.ok:
        logger.warning(f"Unable to connect to {url}")
        r.raise_for_status()
    total_size = int(r.headers.get("Content-Length", "20000000"))
    tmp_file = os.path.join(tmpdir, f"ace.zip")
    with click.progressbar(
        r.iter_content(1024), length=total_size
    ) as bar, open(tmp_file, "wb") as f:
        for chunk in bar:
            f.write(chunk)
            bar.update(len(chunk))
    logger.info(f"Saved to {tmp_file}")
    click.secho("OK", fg="green")


def get_zipfile(tag):
    """
    Get the URL for the zip file of the referenced tag.
    """
    return f"https://github.com/ajaxorg/ace-builds/archive/{tag}.zip"


def unzip(path):
    """
    Unzips the file into the right place in the repository.
    """
    logger.info(f"Unzipping {path}.")
    click.echo(f"Unzipping {path}.")
    zipdir = os.path.join(os.path.dirname(path), "ace")
    with zipfile.ZipFile(path) as zf:
        zf.extractall(zipdir)
    release_dir = glob.glob(os.path.join(zipdir, "*", ""))[0]
    source = os.path.join(zipdir, release_dir, "src-min-noconflict")
    target = ACE_DIR
    logger.info(f"Copying from {source} to {target}.")
    click.echo(f"Copying from {source} to {target}.")
    try:
        shutil.rmtree(target)
    except FileNotFoundError:
        pass
    shutil.move(source, target)


def run():
    logger.info("Checking and updating Python assets.")
    click.echo("Starting...")
    # Check current local version with remote version.
    local_tag_info = {}
    if os.path.exists(TAG_FILE):
        with open(TAG_FILE) as tf:
            local_tag_info = json.load(tf)
            logger.info(local_tag_info)
    else:
        local_tag_info["ace"] = "0"
    remote_tag = get_latest_tag()
    # Ensure the Python platform directories exist.
    force_download = False
    try:
        if force_download:
            local_tag_info["ace"] = "0"
        if remote_tag > local_tag_info.get("ace", "0"):
            logger.info(f"Updating to {remote_tag}.")
            click.echo(f"Updating to {remote_tag}.")
            to_download = get_zipfile(remote_tag)
            with tempfile.TemporaryDirectory() as tmpdir:
                # Download the assets:
                download_file(to_download, "/tmp/foobarbaz")
                asset = os.path.join("/tmp/foobarbaz", "ace.zip")
                unzip(asset)
            local_tag_info["ace"] = remote_tag
            with open(TAG_FILE, "w") as tf:
                json.dump(local_tag_info, tf, indent=2)
            click.secho(
                f"Finished. Updated to release {remote_tag}.", fg="green"
            )
        else:
            # Nothing to do.
            logger.info("Nothing to do.")
            click.secho("Already at the latest version.", fg="green")
    except Exception as ex:
        logger.exception(ex)
        click.secho(
            f"Something went wrong: {ex}.\n\nCheck the logs: {LOGFILE}",
            fg="red",
        )


if __name__ == "__main__":
    run()

