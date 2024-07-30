import csv
import os
import time

from urllib import request
from itertools import chain
from typing import Iterable, Tuple

from PIL import Image
from github import Github, UnknownObjectException
import certifi

git_token = input('What is your github token (if none $ENV:GITHUB_TOKEN is used)? ')

def read_metadata(metadata_file: str, label_col: int, url_col: int) -> Iterable[Tuple[str, str]]:
    with open(metadata_file, newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)

        for row in reader:
            label = str(row[label_col]).strip().replace(" ", "_")
            link = str(row[url_col])
            yield (label, link)

def download_image(url: str, backoff_secs: float = 1, retry_cnt: int = 5) -> Image.Image:
    if "https://drive.google.com/" in url:
        start = url.find("file/d/")
        end = url.find("/view?usp")
        id = url[start + 7:end]
        url = f"https://drive.google.com/uc?export=download&confirm=pbef&id={id}"

    for attempt in range(1, retry_cnt + 1):
        try:
            with request.urlopen(url, cafile=certifi.where()) as f:
                return Image.open(f)
        except Exception as e:
            print(f"Failed to download {url} on attempt {attempt}: {e}")
            time.sleep(backoff_secs := backoff_secs * 2)
    return None

def compress_image(image: Image.Image) -> Image.Image:
    image.thumbnail((1300, 2600))
    return image

def upload_image(image: Image.Image, label: str):
    try:
        git = Github(os.getenv('GITHUB_TOKEN', git_token))
    except:
        print("There were permission errors with your github token.")
        raise

    repo = git.get_repo("TeachmanLab/MindtrailsMobile_Resources")
    git_file = f"HTC/protocols/Spanish/media/images/{label}.jpeg"

    try:
        file = repo.get_contents(git_file)
        sha = file.sha
        action = "Updating"
    except UnknownObjectException as e:
        sha = None
        action = "Creating"

    try:
        if action == "Updating":
            repo.update_file(path=git_file, message=f"{action} image", content=image.tobytes(), sha=sha, branch="main")
            print(f"{label} {action.lower()} on GitHub")
        else:
            repo.create_file(path=git_file, message=f"{action} image", content=image.tobytes(), branch="main")
            print(f"{label} {action.lower()} on GitHub")
    except Exception as e:
        print(f"Error {action.lower()} {git_file} on GitHub: {str(e)}")

short_metadata = read_metadata("/Users/valentinamendoza/Downloads/MT Spanish/Spanish_Short_Scenarios.csv", 3, 9)
long_metadata = read_metadata("/Users/valentinamendoza/Downloads/MT Spanish/Spanish_Long_Scenarios.csv", 3, 5)

for label, url in chain(short_metadata, long_metadata):
    try:
        print(f"Downloading {label}")
        if image := download_image(url):
            print(f"Compressing {label}")
            image = compress_image(image)

            print(f"Uploading {label}")
            upload_image(image, label)
    except Exception as e:
        print(e)
