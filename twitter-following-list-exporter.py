import csv
import json
import subprocess
from tqdm import tqdm
import os

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
ENDC = '\033[0m'

# Path to the file containing URLs
url_file_path = "twitter_following_list_converted.txt"

# Path to the CSV file to save following list info
csv_file_path = "twitter_following_list_data.csv"

def run_gallery_dl(target_url):
    # capture JSON output
    command = f'gallery-dl --range 0 -j "{target_url}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def extract_author_info(json_data):
    try:
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, (list, dict)):
            data = json_data
        else:
            raise ValueError("Invalid JSON data format")

        # Access
        author_info = data[0][1]['author']
        return author_info
    except (json.JSONDecodeError, KeyError, IndexError, ValueError) as e:
        return None

def get_existing_urls(csv_file):
    # Get existing URLs from the CSV file using a set
    existing_urls = set()
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_urls.add(row['Target_URL'])
    return existing_urls

def is_info_already_saved(existing_urls, target_url):
    # Check if the information for a specific target_url already exists in the set
    return target_url in existing_urls

def convert_url(url):
    # Convert the given URL format to the desired format
    parts = url.split(':')
    user_id = parts[-1].split('/')[0]
    return f"https://twitter.com/i/user/{user_id}"

def save_to_csv(target_url, author_info):
    # Save author information to CSV file
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Target_URL', 'Permanent_Profile_Link'] + list(author_info.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        # Convert the target_url and author_info to CSV
        converted_url = convert_url(target_url)
        writer.writerow({'Target_URL': target_url, 'Permanent_Profile_Link': converted_url, **author_info})

if __name__ == "__main__":
    existing_urls = get_existing_urls(csv_file_path)
    skipped_urls_count = 0
    new_rows_count = 0
    failed_urls = []

    with open(url_file_path, 'r', encoding='utf-8') as url_file:
        total_lines = sum(1 for line in url_file)  # Count total lines in the file
        url_file.seek(0)  # Reset file pointer to the beginning

        # Progress bar
        for target_url in tqdm(url_file, desc="Processing URLs", unit="URL", total=total_lines):
            target_url = target_url.strip()
            
            if not is_info_already_saved(existing_urls, target_url):
                json_data = run_gallery_dl(target_url)
                author_info = extract_author_info(json_data)

                if author_info:
                    save_to_csv(target_url, author_info)
                    new_rows_count += 1
                else:
                    # print(f"Failed to extract author info from {target_url}")
                    failed_urls.append(target_url)
            else:
                skipped_urls_count += 1

    # Status text
    status_emoji = GREEN + "✅" + ENDC if not failed_urls else RED + "❌" + ENDC
    status_message = GREEN + "DONE" + ENDC if not failed_urls else RED + "Done but something wrong!!" + ENDC

    # Updated text
    print(f"\n{status_emoji} {status_message}\nTwitter Following List Data has been updated in {BLUE}{csv_file_path}{ENDC}.\n{GREEN}{new_rows_count}{ENDC} URLs added.\n{GREEN}{skipped_urls_count}{ENDC} URLs already exist in the CSV file.\n{RED}{len(failed_urls)}{ENDC} URLs failed.")

    # Llist of failed URLs
    if failed_urls:
        print("\nFailed URLs (Copy and paste them to CSV file to avoid showing them next time):")
        for failed_url in failed_urls:
            converted_failed_url = convert_url(failed_url)
            print(f"{failed_url}\t{converted_failed_url}")
