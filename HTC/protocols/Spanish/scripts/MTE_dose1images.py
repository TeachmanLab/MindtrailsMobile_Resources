import os
import pandas as pd
import requests
from github import Github
from PIL import Image


def download_image(url, title):
    try:
        response = requests.get(url)
        response.raise_for_status()  # raise an error for bad responses
        # create a filename for the downloaded image
        filename = f"{title.replace(' ', '_')}.jpg"  # replace spaces with underscores
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None


def compress_image(image_path):
    try:
        with Image.open(image_path) as img:
            img.thumbnail((1300, 2600))  # resize image
            compressed_path = f"{os.path.splitext(os.path.basename(image_path))[0]}.jpg"
            img.save(compressed_path, "JPEG")  # save as JPEG
            return compressed_path
    except Exception as e:
        print(f"Error compressing image {image_path}: {e}")
        return None


def upload_image_to_github(repo, file_path, commit_message):
    try:
        with open(file_path, 'rb') as file:
            repo.create_file(f"HTC/protocols/Spanish/media/new_images/{os.path.basename(file_path)}",
                             commit_message, file.read())
        print(f"Uploaded {os.path.basename(file_path)} to GitHub in {repo.name}/HTC/protocols/Spanish/media/new_images.")
        return True
    except Exception as e:
        print(f"Failed to upload {file_path}: {e}")
        return False


token = ''  # replace with your actual GitHub token
g = Github(token)
repo_name = "TeachmanLab/MindtrailsMobile_Resources"
repo = g.get_repo(repo_name)


csv_file = '/Users/valentinamendoza/Downloads/MT Spanish/Spanish_dose1_scenarios.csv'
df = pd.read_csv(csv_file)

# list to track failed uploads
failed_images = []


for index, row in df.iterrows():
    if index >= 1:  # skip the header
        title = row['Hoos TC Title']
        image_url = row['New Spanish photo link']

        # check if the image URL is valid (not NaN and not empty)
        if pd.isna(image_url) or not image_url.strip():
            print(f"Invalid URL for title '{title}'. Skipping...")
            continue  # skip to the next iteration


        downloaded_file = download_image(image_url, title)

        if downloaded_file:
            # compress the image before uploading
            compressed_file = compress_image(downloaded_file)

            if compressed_file:
                # upload the compressed image to GitHub
                success = upload_image_to_github(repo, compressed_file, f"Added {title.replace(' ', '_')}.jpg")

                if not success:
                    # if upload failed, add to failed images list
                    failed_images.append({"title": title, "url": image_url})

                # remove the compressed file after upload
                if os.path.exists(compressed_file):
                    os.remove(compressed_file)

            # remove the original downloaded file if it exists
            if os.path.exists(downloaded_file):
                os.remove(downloaded_file)

# print the list of failed images
if failed_images:
    print("Failed to upload the following images:")
    for failed in failed_images:
        print(f"Title: {failed['title']}, URL: {failed['url']}")
else:
    print("All images uploaded successfully.")
