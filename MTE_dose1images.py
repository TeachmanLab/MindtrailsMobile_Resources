import os
import pandas as pd
import requests
from github import Github
from PIL import Image  # Make sure to install Pillow if not already done

# Function to download an image
def download_image(url, title):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        # Create a filename for the downloaded image
        filename = f"{title.replace(' ', '_')}.jpg"  # Replace spaces with underscores
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

# Function to compress an image
def compress_image(image_path):
    try:
        with Image.open(image_path) as img:
            img.thumbnail((1300, 2600))  # Resize image while maintaining aspect ratio
            compressed_path = f"{os.path.splitext(os.path.basename(image_path))[0]}.jpg"  # Keep the original title without "compressed_"
            img.save(compressed_path, "JPEG")  # Save as JPEG
            return compressed_path
    except Exception as e:
        print(f"Error compressing image {image_path}: {e}")
        return None

# Function to upload an image to GitHub
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

# Authenticate to GitHub
token = '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'  # Replace with your actual GitHub token
g = Github(token)
repo_name = "TeachmanLab/MindtrailsMobile_Resources"  # Your repository name
repo = g.get_repo(repo_name)

# Read the CSV file
csv_file = '/Users/valentinamendoza/Downloads/MT Spanish/Spanish_dose1_scenarios.csv'
df = pd.read_csv(csv_file)

# List to track failed uploads
failed_images = []

# Iterate through the CSV
for index, row in df.iterrows():
    if index >= 1:  # Skip the header
        title = row['Hoos TC Title']
        image_url = row['New Spanish photo link']

        # Check if the image URL is valid (not NaN and not empty)
        if pd.isna(image_url) or not image_url.strip():
            print(f"Invalid URL for title '{title}'. Skipping...")
            continue  # Skip to the next iteration

        # Download the image
        downloaded_file = download_image(image_url, title)

        if downloaded_file:
            # Compress the image before uploading
            compressed_file = compress_image(downloaded_file)

            if compressed_file:
                # Upload the compressed image to GitHub
                success = upload_image_to_github(repo, compressed_file, f"Added {title.replace(' ', '_')}.jpg")

                if not success:
                    # If upload failed, add to failed images list
                    failed_images.append({"title": title, "url": image_url})

                # Remove the compressed file after upload
                if os.path.exists(compressed_file):
                    os.remove(compressed_file)

            # Remove the original downloaded file if it exists
            if os.path.exists(downloaded_file):
                os.remove(downloaded_file)

# Print the list of failed images
if failed_images:
    print("Failed to upload the following images:")
    for failed in failed_images:
        print(f"Title: {failed['title']}, URL: {failed['url']}")
else:
    print("All images uploaded successfully.")
