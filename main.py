import os
import requests
import sys
from tqdm import tqdm

from bs4 import BeautifulSoup as bs

# check for proper command line arguments
import arg_manager
QUERY, NUM_IMAGES = arg_manager.parser()

# google image url
GOOGLE_IMAGE = \
    'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

# request header needed for google
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

# name of output directory
SAVE_FOLDER = str(QUERY)

def main():
    try:
        os.mkdir(SAVE_FOLDER)
        download_images()
    except OSError as error:
        print(error)

def download_images():
    print('Starting search...')

    # create and print search link
    searchurl = GOOGLE_IMAGE + 'q=' + QUERY
    print(searchurl)

    # request webpage from google
    response = requests.get(searchurl, headers=usr_agent)
    html = response.text

    # parse html page with beautiful soup
    page = bs(html, 'html.parser')
    containers = page.findAll('img', {'class': 'rg_i'}, limit=(NUM_IMAGES + 20))

    image_links = []
    count = 0

    for container in containers:
        link = container.get('data-src')
        if link:
            image_links.append(link)
            count += 1
        
        if count == NUM_IMAGES:
            break

    print(f'\nFound {len(image_links)} images.')

    # progress bar
    bar = tqdm(
        total=NUM_IMAGES,
        desc='Downloading images... ',
        unit=' images',
        ascii=True
    )

    for i, link in enumerate(image_links):
        response = requests.get(link)

        imagename = os.path.join(SAVE_FOLDER, f'images_{i}.jpg')

        # write link data to new file
        with open(imagename, 'wb') as file:
            file.write(response.content)
        
        bar.update(1)

    bar.close()
    print(f'\n{len(image_links)} images saved to ./{SAVE_FOLDER} directory.')

if __name__ == '__main__':
    main()
