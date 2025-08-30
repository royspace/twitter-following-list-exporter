import csv
import os
import requests
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm
import argparse

# ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
ENDC = '\033[0m'

parser = argparse.ArgumentParser(description="Export Twitter following list to HTML")
parser.add_argument("--no-pfp", action="store_true", help="Do not download or include profile pictures")
args = parser.parse_args()

errors = []

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
        # print(f"Error downloading image: {e}")
        errors.append(str(e))
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

    # Reverse the order of rows,, remove if needed
    # reversed_csv_reader = reversed(list(csv_reader))

    tqdm_iterator = tqdm(csv_reader, total=total_rows, desc="Downloading Images", unit=' images')

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

        if not args.no_pfp:
            if image_filename not in downloaded_image_ids and not os.path.exists(image_path):
                # Download the image
                success = download_image(row['profile_image'], image_path)
                if success:
                    downloaded_image_ids.add(image_filename)

        # Update the row to use local image path unless --no-pfp is set
        if not args.no_pfp:
            row['profile_image'] = image_path if os.path.exists(image_path) else row['profile_image']

        # Append the updated row to the CSV data
        csv_data.append(row)

# Render HTML using Jinja2 template
html_output = template.render(data=csv_data)

# Save HTML output to a file
with open('twitter_following_list.html', 'w', encoding='utf-8') as output_file:
    output_file.write(html_output)

# Determine the status emoji and message based on the presence of failed URLs
status_emoji = GREEN + "✅" + ENDC if not errors else RED + "❌" + ENDC
status_message = GREEN + "DONE (V1)" + ENDC if not errors else RED + "Done but something wrong!!" + ENDC

print(f"\n{status_emoji} {status_message}\n")

# Print total errors only if there are errors
if errors:
    print(f"Total url errors encountered when trying download: {RED}{len(errors)}{ENDC}")