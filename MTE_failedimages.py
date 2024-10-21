import requests
import os
import csv
from github import Github

# GitHub authentication
GITHUB_TOKEN = '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'
REPO_NAME = 'TeachmanLab/MindtrailsMobile_Resources'
FOLDER_PATH = 'HTC/protocols/Spanish/media/new_images'  # Upload folder

# Authenticate GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)


def download_image(title, url):
    """Download the image and save it locally with a renamed title, only if it's of the correct content type."""
    try:
        response = requests.get(url)

        # Check if the content type is image/jpeg
        content_type = response.headers.get('Content-Type')
        if content_type == 'image/jpeg' and response.status_code == 200:
            # Sanitize the title for a valid filename
            filename = f"{title.replace(' ', '_').replace(':', '')}.jpg"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename} (Content-Type: {content_type})")
            return filename
        else:
            print(f"Skipped {title}. Unsupported Content-Type: {content_type}")
            return None
    except Exception as e:
        print(f"Error downloading {title}: {e}")
        return None


def upload_image_to_github(filename):
    """Upload the downloaded image to the GitHub repository, handling both creation and updates."""
    try:
        # Check if the file already exists in the repo
        file_path = f"{FOLDER_PATH}/{filename}"
        contents = None
        try:
            contents = repo.get_contents(file_path)
        except Exception as e:
            # File does not exist, so we proceed with creating it
            pass

        with open(filename, 'rb') as file:
            content = file.read()

            if contents:
                # File exists, so we update it
                repo.update_file(file_path, f"Update {filename}", content, contents.sha)
                print(f"Updated {filename} in GitHub in {FOLDER_PATH}")
            else:
                # File does not exist, so we create it
                repo.create_file(file_path, f"Upload {filename}", content)
                print(f"Uploaded {filename} to GitHub in {FOLDER_PATH}")
    except Exception as e:
        print(f"Error uploading {filename}: {e}")


def process_failed_images(csv_file):
    """Process the CSV file, download, and upload images."""
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and 'Title:' in row[0] and 'URL:' in row[0]:
                # Extract title and URL from the row
                title = row[0].split('Title: ')[1].split(', URL: ')[0]
                url = row[0].split('URL: ')[1]

                # Download and rename the image
                downloaded_file = download_image(title, url)

                if downloaded_file:
                    # Upload to GitHub
                    upload_image_to_github(downloaded_file)

                    # Clean up by removing the local file after upload
                    os.remove(downloaded_file)


# Specify the CSV file containing the failed images
csv_file = '/Users/valentinamendoza/Downloads/MT Spanish/failed_images.csv'

# Process the CSV and handle images
process_failed_images(csv_file)