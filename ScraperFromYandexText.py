import os
import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

downloaded_images_folder = 'F:\\roberta'
if not os.path.exists(downloaded_images_folder):
    os.makedirs(downloaded_images_folder)

MAX_THREADS = concurrent.futures.ThreadPoolExecutor(max_workers=None)  # Use max_workers=None for maximum threads

def download_image(link, folder, idx):
    try:
        response = requests.get(link, timeout=10, stream=True)

        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            image_extension = link.split('.')[-1]
            image_filename = f'image_{idx + 1}.{image_extension}'
            image_path = os.path.join(folder, image_filename)

            with open(image_path, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                    for chunk in response.iter_content(1024):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

            return image_filename
        else:
            return None
    except requests.exceptions.Timeout:
        print(f"Connection timed out for link: {link}")
        return None

def update_completed_downloads(link):
    with open('D:\cool python projects\imx_scraper\completedDownloads.txt', 'a+') as f:
        f.seek(0)
        links_in_file = f.read().splitlines()
        if link not in links_in_file:
            f.write(link + '\n')

def process_link(link):
    try:
        response = requests.get(link, timeout=10)
        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')
        title_element = soup.find('div', class_='title')

        if title_element:
            title = title_element.get_text(strip=True)
            title = title.replace('/', '_')
            title_folder = os.path.join(downloaded_images_folder, title)

            if not os.path.exists(title_folder):
                os.makedirs(title_folder)

            image_containers = soup.find_all('div', class_='tooltip')

            futures = []
            for idx, container in enumerate(image_containers):
                img_tag = container.find('img', class_='imgtooltip')
                if img_tag:
                    img_src = img_tag['src']
                    img_src = img_src.replace('/t/', '/i/')
                    img_src = img_src.replace('>', '/')
                    futures.append(MAX_THREADS.submit(download_image, img_src, title_folder, idx))

            for future in concurrent.futures.as_completed(futures):
                image_filename = future.result()
                if image_filename:
                    update_completed_downloads(link)

            print(f"Downloaded {len(image_containers)} images in '{title}'")

            with open(os.path.join(title_folder, 'details.txt'), 'w') as f:
                for container in image_containers:
                    img_tag = container.find('img', class_='imgtooltip')
                    if img_tag:
                        img_src = img_tag['src']
                        f.write(img_src + '\n')

        else:
            print("Title element not found on the page.")
    except requests.exceptions.Timeout:
        print(f"Connection timed out for link: {link}")

def extract_and_save_links(text_file_path):
    with open(text_file_path, 'r', encoding='utf-8') as file:
        page_content = file.read()

    # Use regular expression to find links matching the pattern imx.to›g/[\w-]+
    links = re.findall(r'imx\.to›g/[\w-]+', page_content)

    # Modify and save the links to links.txt
    with open('D:\cool python projects\imx_scraper\links.txt', 'w') as links_file:
        for link in links:
            modified_link = 'https://' + link.replace('›', '/').replace('>', '/')
            links_file.write(modified_link + '\n')

def main():
    text_file_path = 'D:\\cool python projects\\imx_scraper\\text_corpus.txt'  # Replace with your text file path
    extract_and_save_links(text_file_path)

    with open('D:\cool python projects\imx_scraper\links.txt', 'r') as file:
        links = file.read().splitlines()

    for link in links:
        with open('D:\cool python projects\imx_scraper\completedDownloads.txt', 'r') as file:
            completed_links = file.read().splitlines()

        if link not in completed_links:
            process_link(link)

    print("All images downloaded and saved.")

if __name__ == "__main__":
    main()
