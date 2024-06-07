import requests
from bs4 import BeautifulSoup
import argparse
import re
import subprocess

def search_getcomics(keyword, page_number=1):
    search_url = f"https://getcomics.org/page/{page_number}/?s={keyword.replace(' ', '+')}"
    response = requests.get(search_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)

    year_pattern = re.compile(r'\b(19|20)\d{2}\b')
    categorized_links = {}

    for link in links:
        href = link['href']
        text = link.get_text().strip()
        
        if 'getcomics.org' in href and keyword.lower() in text.lower():
            match = year_pattern.search(href)
            if match:
                year = match.group(0)
                if year not in categorized_links:
                    categorized_links[year] = []
                categorized_links[year].append({'text': text, 'href': href})
            else:
                if 'Unknown' not in categorized_links:
                    categorized_links['Unknown'] = []
                categorized_links['Unknown'].append({'text': text, 'href': href})

    return categorized_links

def get_download_links(link):
    response = requests.get(link)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    download_links = []

    download_elements = soup.find_all('a', class_='aio-red', href=True)
    for element in download_elements:
        download_link = element['href']
        # Filter out links from readcomicsonline.ru
        if 'readcomicsonline.ru' not in download_link:
            download_links.append(download_link)

    return download_links

def download_with_aria2c(url, output_dir='.'):
    command = ['aria2c', '-d', output_dir, url]
    subprocess.run(command)

def main():
    parser = argparse.ArgumentParser(description="Search GetComics for a keyword and return all matching links categorized by year.")
    parser.add_argument('keyword', type=str, help="The keyword to search for.")
    parser.add_argument('-p', '--page', type=int, default=1, help="The page number to search on.")
    args = parser.parse_args()

    keyword = args.keyword
    page_number = args.page

    categorized_links = search_getcomics(keyword, page_number)
    
    comics = []
    for year, links in categorized_links.items():
        for item in links:
            comics.append({'year': year, 'text': item['text'], 'href': item['href']})

    if not comics:
        print("No comics found.")
        return

    for idx, comic in enumerate(comics, start=1):
        print(f"{idx}. [{comic['year']}] {comic['text']}")

    try:
        choice = int(input("\nEnter the number of the comic you want to download: "))
        selected_comic = comics[choice - 1]
        print(f"\nYou selected: {selected_comic['text']} ({selected_comic['year']})")
        
        download_links = get_download_links(selected_comic['href'])
        if download_links:
            print("Download links found:")
            for idx, download_link in enumerate(download_links, start=1):
                print(f"{idx}. {download_link}")
            download_choice = int(input("\nEnter the number of the download link you want to use: "))
            download_url = download_links[download_choice - 1]
            print(f"\nDownloading from: {download_url}")
            download_with_aria2c(download_url)
            print("Download completed.")
        else:
            print("No download links found for the selected comic.")
    except (ValueError, IndexError):
        print("Invalid selection. Exiting.")

if __name__ == "__main__":
    main()
