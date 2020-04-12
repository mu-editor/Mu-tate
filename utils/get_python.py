"""
Checks the latest release from the "Python Build Standalone" project
(https://github.com/indygreg/python-build-standalone) which provides statically
compiled, stand-alone builds of the Python programming language.
"""
import click
import glob
import json
import logging
import os
import requests
import shutil
import tarfile
import tempfile
import zstd


# Refers to the root of the project.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The log file (for all the details).
LOGFILE = os.path.join(BASE_DIR, "get_python.log")
# Python directory.
PYTHON_DIR = os.path.join(BASE_DIR, "python")
# Python version tag file (keeps track of tags of latest release).
TAG_FILE = os.path.join(PYTHON_DIR, "tag.json")
# Platforms for whom Mu packages a Python runtime.
PLATFORMS = {
    "linux64",
    "windows-amd64",
    "windows-x86",
    "macos",
}
# Paths to platform specific versions of Python.
VERSIONS = {
    platform: os.path.join(PYTHON_DIR, platform) for platform in PLATFORMS
}


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
    url = (
        "https://github.com/indygreg/python-build-standalone"
        "/releases/latest"
    )
    logger.info("Requesting tag information: {}".format(url))
    response = requests.get(url)
    logger.info("Response url: {}".format(response.url))
    tag = response.url.rsplit("/", 1)[-1]
    logger.info(f"Remote tag: {tag}")
    return tag


def download_file(url, platform, tmpdir):
    """
    Download a Python distribution for a platform into the tmpdir.
    """
    click.echo(f"Downloading {url}")
    logger.info(f"Downloading {url}")
    r = requests.get(url, stream=True)
    if r.status_code != requests.codes.ok:
        logger.warning(f"Unable to connect to {url}")
        r.raise_for_status()
    total_size = int(r.headers.get("Content-Length"))
    tmp_file = os.path.join(tmpdir, f"{platform}.tar.zst")
    with click.progressbar(
        r.iter_content(1024), length=total_size
    ) as bar, open(tmp_file, "wb") as f:
        for chunk in bar:
            f.write(chunk)
            bar.update(len(chunk))
    logger.info(f"Saved to {tmp_file}")
    click.secho("OK", fg="green")


def get_assets(tag):
    """
    Get the assets for the supported platforms with the referenced tag.
    """
    url = (
        "https://api.github.com/repos/indygreg/python-build-standalone"
        f"/releases/tags/{tag}"
    )
    r = requests.get(url)
    data = r.json()
    releases = data["assets"]
    result = {}
    for asset in releases:
        for platform in PLATFORMS:
            if platform in asset["name"] and "musl" not in asset["name"]:
                result[platform] = asset["browser_download_url"]
    return result


def unzip(path, platform):
    """
    Unzips and untars the file for the specified platform into the right place
    in the repository.
    """
    logger.info(f"Unzipping {path}.")
    click.echo(f"Unzipping {path}.")
    tarfilename = path.replace(".zst", "")
    filesize = os.path.getsize(path)
    # Unzip to tar file.
    with open(tarfilename, "wb") as tf:
        with open(path, "rb") as fh:
            dctx = zstd.ZstdDecompressor()
            with click.progressbar(
                dctx.read_to_iter(fh, read_size=16384), length=filesize
            ) as bar:
                for chunk in bar:
                    tf.write(chunk)
                    bar.update(len(chunk))
    # Untar the file.
    logger.info(f"Untarring {tarfilename}.")
    click.echo(f"Untarring {tarfilename}.")
    output_dir = os.path.join(os.path.dirname(path), platform)
    with tarfile.open(tarfilename) as tar:
        target = os.path.join(PYTHON_DIR, platform)
        tar.extractall(path=output_dir)
    # Copy the install directory from the package to the correct location in
    # the repository.
    source = os.path.join(output_dir, "python", "install")
    target = os.path.join(PYTHON_DIR, platform)
    logger.info(f"Copying Python from {source} to {target}.")
    click.echo(f"Copying Python from {source} to {target}.")
    shutil.rmtree(target)
    shutil.move(source, target)


def run():
    logger.info("Checking and updating Python assets.")
    click.echo("Starting...")
    # Check current local version with remote version.
    if os.path.exists(TAG_FILE):
        with open(TAG_FILE) as tf:
            local_tag_info = json.load(tf)
            logger.info(local_tag_info)
    else:
        local_tag_info["tag"] = "0"
    remote_tag = get_latest_tag()
    # Ensure the Python platform directories exist.
    force_download = False
    try:
        for platform in PLATFORMS:
            platform_dir = os.path.join(PYTHON_DIR, platform)
            if not os.path.exists(platform_dir):
                os.makedirs(platform_dir)
                force_download = True
            elif not os.listdir(platform_dir):
                # The directory is empty, so force a download of Python.
                force_download = True
        if force_download:
            local_tag_info["tag"] = "0"
        if remote_tag > local_tag_info.get("tag", "0"):
            logger.info(f"Updating to {remote_tag}.")
            click.echo(f"Updating to {remote_tag}.")
            to_download = get_assets(remote_tag)
            with tempfile.TemporaryDirectory() as tmpdir:
                # Download the assets:
                for platform, url in to_download.items():
                    download_file(url, platform, "/tmp/foobarbaz")
                # Decompress, unzip and copy each asset to the right location:
                to_process = glob.glob(
                    os.path.join("/tmp/foobarbaz", "*.tar.zst")
                )
                for asset in to_process:
                    platform = os.path.basename(asset).split(".", 1)[0]
                    click.echo(f"Processing Python for {platform}.")
                    unzip(asset, platform)
            local_tag_info["tag"] = remote_tag
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
