import csv
import os
import requests
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

# Function to download profile images
def download_image(image_url, image_path):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Raise an exception for bad responses
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return False

# Read CSV file
csv_file = 'twitter_following_list_data.csv'  # Replace with your CSV file path
image_folder = 'images'

# Create the 'images' folder if it doesn't exist
os.makedirs(image_folder, exist_ok=True)

# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

# Variables to store downloaded image IDs
downloaded_image_ids = set()

# Read CSV data
csv_data = []
with open(csv_file, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    total_rows = sum(1 for _ in csv_reader)  # Count total rows for tqdm
    file.seek(0)  # Reset file pointer
    tqdm_iterator = tqdm(csv_reader, total=total_rows, desc="Downloading Images")

    for row in tqdm_iterator:
        # Skip rows with missing ID or profile_image
        if 'id' not in row or 'profile_image' not in row:
            continue

        # Handle errors when converting ID to int
        try:
            row['id'] = int(row['id'])
        except ValueError:
            # tqdm_iterator.write(f"Skipping row due to invalid ID: {row}")
            continue

        # Check if the image has already been downloaded
        image_filename = f"{row['id']}.jpg"
        image_path = os.path.join(image_folder, image_filename)

        if image_filename not in downloaded_image_ids and not os.path.exists(image_path):
            # Download the image
            success = download_image(row['profile_image'], image_path)
            if success:
                downloaded_image_ids.add(image_filename)

        # Update the row to use local image path
        row['profile_image'] = image_path if os.path.exists(image_path) else row['profile_image']

        # Append the updated row to the CSV data
        csv_data.append(row)

# Render HTML using Jinja2 template
html_output = template.render(data=csv_data)

# Save HTML output to a file
with open('twitter_following_list.html', 'w', encoding='utf-8') as output_file:
    output_file.write(html_output)
