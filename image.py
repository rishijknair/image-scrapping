import requests
from bs4 import BeautifulSoup
import os
import re

# URL of the web page you want to scrape
url = "PLEASE_PASTE_THE_URL_OF_THE_SITE_YOU_WANT_TO_OBTAIN_IMAGE_FROM"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all image elements with the 'srcset' attribute (contains image URLs)
    img_tags = soup.find_all("img", {"srcset": re.compile(r'.*')})

    # Create a directory to save the images (if it doesn't exist)
    if not os.path.exists("images"):
        os.makedirs("images")

    # Download and save each image as JPEG
    for img in img_tags:
        img_url = img["src"]
        img_data = requests.get(img_url).content
        # Generate a safe filename from the URL
        filename = os.path.join("images", re.sub(r'[^a-zA-Z0-9_.-]', '_', os.path.basename(img_url))) + ".jpg"
        with open(filename, "wb") as f:
            f.write(img_data)
else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
