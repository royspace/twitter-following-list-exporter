# Twitter Following List Exporter

<a href="https://www.buymeacoffee.com/royspace" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>


## Features

- Export your following list on Twitter to TXT, CSV, and HTML formats in case your Twitter/X account is suspended at no cost :)
- Easy to use and update the following list.
- Easy to keep track in case your following changes username or is suspended
- Save PFP image locally

- **Beautiful HTML for Visualization with ***isotope*** search and ***Mansory*** layout**

<img width="800" alt="Screenshot 2024-01-08 at 02 17 58" src="https://github.com/royspace/twitter-following-list-exporter/assets/85507215/74157e60-d8ae-4f12-8c92-51a3aa017db1">

## Requirements

- Python 3.x
- [gallery-dl](https://github.com/mikf/gallery-dl)
- [tqdm](https://github.com/tqdm/tqdm)

## Usage

1. **Install Dependencies:**

   gallery-dl
     ```bash
     pip install gallery-dl
     ```
   tqdm
     ```bash
     pip install tqdm
     ```

2. **Clone the Repository**
     ```bash
     git clone https://github.com/royspace/twitter-following-list-exporter.git
     ```

3. **Navigate to the Repository**
     ```bash
     cd twitter-following-list-exporter
     ```

4. **Suggestion `config.json` file for gallery-dl**
   - You **must** create a `config.json` file and enter your `YourUsername` and `YourPassword` to export your following list. For more details and instructions: [click here](https://github.com/mikf/gallery-dl?tab=readme-ov-file#configuration)
     ```json
     {
         "extractor": {
             "twitter": {
                 "username": "YourUsername",
                 "password": "YourPassword",
                 "filename": "{author['name']}-{author['id']}-{tweet_id}-{num}-{date:?//%Y%m%d_%H%M%S}.{extension}",
                 "skip": "abort:2"
             }
         },
         "output": {
             "shorten": false
         }
     }
     ```

5. Export to TXT, CSV and HTML file
- Fill `YourUsername`

     ```bash
     gallery-dl -g https://twitter.com/YourUsername/following > twitter_following_list.txt
     gallery-dl --get-urls -g https://twitter.com/YourUsername/following > twitter_following_list_converted.txt
     python3 twitter-following-list-exporter.py
     python3 twitter-following-list-exporter-html.py
     python3 convert_v2.py
     ```


- Run this command again to keep the file up to date
- File will include:

`Target_Url` | `Permanent_Profile_Link` |	`date` | `description` | `favourites_count` | `followers_count` | `friends_count` | `id` | `listed_count` | `location` | `media_count` | `name` | `nick` | `profile_banner` | `profile_image` | `statuses_count` | `url` | `verified`
![291020178-65c62b17-f7f1-41b5-a36e-90f069fe98cf](https://github.com/royspace/twitter-following-list-exporter/assets/85507215/20323926-56a4-4204-8444-c260d27c9954)
<img width="800" alt="293262295-f6ad7280-870f-4b03-aded-ec7c11b36ae2" src="https://github.com/royspace/twitter-following-list-exporter/assets/85507215/d05e95c0-955b-47f1-8652-b98d6b74b33a">

## Note
- There may be failed URLs at the moment, copy and paste them to a CSV file to avoid showing them next time.
- Ensure that the number displayed in the tqdm progress bar is correct.
- There may be rate limits imposed by Twitter, so let the process run in the background.
- Since this repository relies on gallery-dl to fetch data, if there are errors during the execution of the gallery-dl command, please report the issue to them instead of here.

## Other scripts

1. [export-twitter-following-list](https://github.com/prinsss/export-twitter-following-list) by [prinsss](https://github.com/prinsss)
- Using a different approach by leveraging the Web API of Twitter itself.
- Has raw JSON.
- **NOT** easy to keep track in case your following changes username or is suspended.


## Contributions
Contributions and improvements to the tool are welcome. Feel free to fork the repository, make enhancements, and submit pull requests.

## Disclaimer
Please use this tool responsibly and ensure compliance with Twitter's terms of service and API usage policies.
