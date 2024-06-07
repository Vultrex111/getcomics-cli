import requests
from bs4 import BeautifulSoup
import argparse
import re

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
        download_links.append(download_link)

    return download_links

def main():
    parser = argparse.ArgumentParser(description="Search GetComics for a keyword and return all matching links categorized by year.")
    parser.add_argument('keyword', type=str, help="The keyword to search for.")
    parser.add_argument('-p', '--page', type=int, default=1, help="The page number to search on.")
    args = parser.parse_args()

    keyword = args.keyword
    page_number = args.page

    categorized_links = search_getcomics(keyword, page_number)
    
    for year, links in categorized_links.items():
        print(f"\nYear {year}:")
        for item in links:
            print("--------------------------------------------------------")
            print(f"  Title: {item['text']}")
            print(f"  Link: {item['href']}")
            download_links = get_download_links(item['href'])
            for download_link in download_links:
                print(f"    Download Link: {download_link}")
            print("--------------------------------------------------------")

if __name__ == "__main__":
    main()
