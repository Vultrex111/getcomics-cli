# getcomics-cli
Download comics from getcomics.org

## Description
This script allows you to search for and download comics from getcomics.org. You can search for a keyword, view the results categorized by year, and choose which comic to download using aria2c.

## Requirements
- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `aria2c` installed on your system

## Installation
1. **Install Python**: Ensure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Install required libraries**: You can install the required Python libraries using pip:
    ```sh
    pip install requests beautifulsoup4
    ```

3. **Install aria2c**: Follow the instructions for your operating system to install `aria2c`.

    - **Ubuntu/Debian**:
        ```sh
        sudo apt-get install aria2c
        sudo dnf install aria2c
        sudo pacman -S aria2c
        ```

    - **macOS** (using Homebrew):
        ```sh
        brew install aria2
        ```

    - **Windows**: Download the Windows binary from the [official aria2 release page](https://github.com/aria2/aria2/releases) and follow the installation instructions.

## Usage
1. **Clone or download the script**: Save the `getcomics-cli.py` script to your local machine.

2. **Run the script**:
    ```sh
    python getcomics-cli.py <keyword> [-p <page_number>]
    ```

    - `<keyword>`: The keyword to search for.
    - `-p <page_number>` (optional): The page number to search on (default is 1).

    Example:
    ```sh
    python getcomics-cli.py "Spider-Man"
    ```

3. **Select a comic**:
    - The script will display a list of comics matching your search keyword, categorized by year.
    - Enter the number corresponding to the comic you want to download.

4. **Select a download link**:
    - The script will display a list of available download links for the selected comic.
    - Enter the number corresponding to the download link you want to use.

5. **Download**:
    - The script will use `aria2c` to download the selected comic.

## Example
1. **Search for comics**:
    ```sh
    python getcomics-cli.py "Batman"
    ```

    Output:
    ```
    1. [2021] Batman #100
    2. [2020] Batman #99
    3. [Unknown] Batman: The Killing Joke

    Enter the number of the comic you want to download: 1
    ```

2. **Select a download link**:
    ```
    Download links found:
    1. https://example.com/download1
    2. https://example.com/download2

    Enter the number of the download link you want to use: 1
    ```

3. **Download**:
    ```
    Downloading from: https://example.com/download1
    Download completed.
    ```

## Notes
- Ensure that you have `aria2c` installed and properly configured on your system.
- This script only filters out links from `readcomicsonline.ru` to ensure valid download links are shown.
- If no comics are found, try searching with a different keyword or adjusting the page number.

## License
This project is licensed under the MIT License.
