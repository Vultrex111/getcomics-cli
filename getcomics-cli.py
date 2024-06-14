import requests
from bs4 import BeautifulSoup
import argparse
import re
import os
import subprocess

# Constants
SEARCH_URL_TEMPLATE = "https://getcomics.org/?s={}"
YEAR_PATTERN = re.compile(r'\b(19|20)\d{2}\b')
SPECIAL_CASES = {
    "spider man": "Spider-Man",
    "ms marvel": "Ms. Marvel",
    "spider gwen": "Spider-Gwen",
}

def normalize_keyword(keyword: str) -> str:
    """Normalize the keyword by applying special cases and converting to lowercase."""
    keyword = keyword.lower()
    for case in SPECIAL_CASES:
        if case in keyword:
            keyword = keyword.replace(case, SPECIAL_CASES[case])
    return keyword

def format_folder_name(name: str) -> str:
    """Format the folder name by capitalizing properly and handling special cases."""
    name = normalize_keyword(name)
    for case, replacement in SPECIAL_CASES.items():
        if case in name:
            name = name.replace(case, replacement)

    # Capitalize the first letter of each word
    name = ' '.join(word.capitalize() for word in name.split())
    return f"{name} Comics"

def search_getcomics(keyword: str) -> dict:
    """Search GetComics for a keyword and return categorized links."""
    variations = generate_variations(keyword)
    categorized_links = {}
    
    for variation in variations:
        search_url = SEARCH_URL_TEMPLATE.format(variation.replace(' ', '+'))
        print(f"Constructed URL: {search_url}")

        response = requests.get(search_url)
        print(f"HTTP Status Code: {response.status_code}")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Page Title: {soup.title.string}")

        links = soup.find_all('a', href=True)
        print(f"Number of Links Found: {len(links)}")

        for link in links:
            href = link['href']
            text = link.get_text().strip()

            if 'getcomics.org' in href and any(var in text.lower() for var in variations):
                match = YEAR_PATTERN.search(href)
                if match:
                    year = match.group(0)
                    if year not in categorized_links:
                        categorized_links[year] = []
                    size = get_comic_size(href)
                    categorized_links[year].append({'text': text, 'href': href, 'size': size})
                else:
                    if 'Unknown' not in categorized_links:
                        categorized_links['Unknown'] = []
                    size = get_comic_size(href)
                    categorized_links['Unknown'].append({'text': text, 'href': href, 'size': size})

    return categorized_links

def get_comic_size(link: str) -> str:
    """Get the size of a comic book."""
    response = requests.get(link)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    size_element = soup.find('p', style="text-align: center;")
    if size_element:
        size_text = size_element.get_text()
        size_match = re.search(r'Size\s*:\s*([\d.]+\s*MB)', size_text)
        if size_match:
            return size_match.group(1)
    
    download_list_items = soup.find_all("li")
    for li in download_list_items:
        size_match = re.search(r'\(([\d.]+\s*MB)\)', li.get_text())
        if size_match:
            return size_match.group(1)
    
    return 'Unknown'

def get_download_links(link: str) -> list:
    """Get download links from a comic page."""
    response = requests.get(link)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    download_links = []

    link_elements = soup.find_all("a", href=True)
    for a in link_elements:
        # For single download links
        if a['href'].startswith("https://getcomics.org/dlds/") and a.get('title') == 'Download Now':
            download_links.append(a['href'])
        
        # For multiple download links (volumes)
        span = a.find("span", style="color: #ff0000;")
        if span and span.get_text().strip() == "Main Server":
            download_links.append(a['href'])

    return download_links

def download_with_aria2c(url: str, output_dir: str = '.') -> None:
    """Download a file using aria2c."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    command = ['aria2c', '-d', output_dir, url]
    subprocess.run(command)

def generate_variations(keyword: str) -> list:
    """Generate variations of the keyword by adding/removing 's' and handling '+' and '-'."""
    words = keyword.split()
    variations = set()
    
    # Add original keyword
    variations.add(keyword)
    
    # Add keyword with pluses
    variations.add(keyword.replace(' ', '+'))
    
    # Add keyword with minuses
    variations.add(keyword.replace(' ', '-'))

    # Generate plural and singular variations
    for word in words:
        if word.endswith('s'):
            singular = word[:-1]
            variations.add(keyword.replace(word, singular))
            variations.add(keyword.replace(word, singular).replace(' ', '+'))
            variations.add(keyword.replace(word, singular).replace(' ', '-'))
        else:
            plural = word + 's'
            variations.add(keyword.replace(word, plural))
            variations.add(keyword.replace(word, plural).replace(' ', '+'))
            variations.add(keyword.replace(word, plural).replace(' ', '-'))

    return list(variations)

def search_multiple_keywords(keyword: str) -> dict:
    """Search GetComics for a keyword, its individual words, and their variations, returning categorized links."""
    keywords = keyword.split()
    all_categorized_links = {}

    # Search for the full keyword and its variations
    keyword_variations = generate_variations(keyword)
    for kw in keyword_variations:
        kw_links = search_getcomics(kw)
        for year, links in kw_links.items():
            if year not in all_categorized_links:
                all_categorized_links[year] = []
            all_categorized_links[year].extend(links)

    # Search for individual words and their variations
    for word in keywords:
        word_variations = generate_variations(word)
        for wv in word_variations:
            word_links = search_getcomics(wv)
            for year, links in word_links.items():
                if year not in all_categorized_links:
                    all_categorized_links[year] = []
                all_categorized_links[year].extend(links)

    return all_categorized_links

def main() -> None:
    """Main program entry point."""
    parser = argparse.ArgumentParser(description="Search GetComics for a keyword and return all matching links categorized by year.")
    parser.add_argument('keyword', type=str, help="The keyword to search for.")
    args = parser.parse_args()

    keyword = normalize_keyword(args.keyword)
    categorized_links = search_multiple_keywords(keyword)

    comics = []
    for year, links in categorized_links.items():
        for item in links:
            comics.append({'year': year, 'text': item['text'], 'href': item['href'], 'size': item['size']})

    if not comics:
        print("No comics found.")
        return

    for idx, comic in enumerate(comics, start=1):
        print(f"{idx}. [{comic['year']}] {comic['text']} - Size: {comic['size']}")

    choice = input("\nEnter the number of the comic you want to download or 'exit' to quit: ").strip().lower()
    if choice == 'exit':
        print("Exiting without downloading.")
        return

    try:
        choice = int(choice)
        selected_comic = comics[choice - 1]
        print(f"\nYou selected: {selected_comic['text']} ({selected_comic['year']}) - Size: {selected_comic['size']}")

        confirm_download = input("Confirm download (Y/n): ").strip().lower()
        if confirm_download in ['', 'y']:
            download_links = get_download_links(selected_comic['href'])
            if download_links:
                formatted_links = [
                    f"{selected_comic['text']} Vol {idx+1}: {link}" for idx, link in enumerate(download_links)
                ]
                print("Download links found:")
                for idx, link in enumerate(formatted_links, start=1):
                    print(f"{idx}. {link}")

                chosen_volumes = input("\nEnter the numbers of the volumes you want to download (comma separated): ").strip()
                chosen_indices = [int(i) for i in chosen_volumes.split(',') if i.isdigit()]

                comic_name = ' '.join(selected_comic['text'].split()[:2])
                output_dir = os.path.join("Comic Book", format_folder_name(comic_name))

                for idx in chosen_indices:
                    if 1 <= idx <= len(download_links):
                        download_with_aria2c(download_links[idx - 1], output_dir)
                print("Download completed.")
            else:
                print("Download links not found.")

    except (ValueError, IndexError):
        print("Invalid selection. Exiting.")

if __name__ == "__main__":
    main()
