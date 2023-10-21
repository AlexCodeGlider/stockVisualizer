import requests
from bs4 import BeautifulSoup
import requests
import zipfile
import io
import os
import time

URL = 'https://firstratedata.com/it/stock/'
EXTRACT_PATH = 'data/frd_sample_stock'             # Destination directory to extract content

response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all anchor tags in the page
links = soup.find_all('a')

# Extract the href attribute from each anchor tag and filter based on the criteria
filtered_links = [link.get('href') for link in links if link.get('href') and link.get('href').startswith('/i/stock/')]
avail_tickers = [link.removeprefix('/i/stock/') for link in filtered_links]

# Drop ticker from the list if it ends with '-DELISTED'
avail_tickers = [ticker for ticker in avail_tickers if not ticker.endswith('-DELISTED')]

def download_and_unzip(url, extract_to):
    # Check if the directory exists, create it if not
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    with requests.get(url, stream=True) as response:
        # Check if the request was successful
        response.raise_for_status()
        
        # Use BytesIO to convert the streamed content to a file-like object
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            # List all members in the ZIP archive
            for member in z.namelist():
                # Check if the member is a .csv file
                if member.endswith('.csv'):
                    z.extract(member, extract_to)

    print(f"Downloaded and extracted {url} to {extract_to}")

if __name__ == '__main__':
    for ticker in avail_tickers:
        URL = f'https://frd001.s3.us-east-2.amazonaws.com/frd_sample_stock_{ticker}.zip'
        download_and_unzip(URL, EXTRACT_PATH)
        time.sleep(1) # Sleep for 1 second to avoid throttling by AWS