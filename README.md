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
### General Steps
1. **Install Python**: Ensure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Install required libraries**: You can install the required Python libraries using pip:
    ```sh
    pip install requests beautifulsoup4
    ```

3. **Install aria2c**: Follow the instructions for your operating system to install `aria2c`.

    - **Ubuntu/Debian**:
        ```sh
        sudo apt-get install aria2
        ```

    - **Fedora**:
        ```sh
        sudo dnf install aria2
        ```

    - **Arch Linux**:
        ```sh
        sudo pacman -S aria2
        ```

    - **macOS** (using Homebrew):
        ```sh
        brew install aria2
        ```

    - **Windows**: Download the Windows binary from the [official aria2 release page](https://github.com/aria2/aria2/releases) and follow the installation instructions.

    - **Android**: Use Termux to install Python and aria2.
        1. Install Termux from the Google Play Store or F-Droid.
        2. Open Termux and run:
            ```sh
            pkg install python aria2
            pip install requests beautifulsoup4
            ```

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

4. **Confirm Download**:
    - If a valid download link is found, it will be displayed.
    - Press Enter to confirm and start the download.

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

2. **Confirm download**:
    ```
    Download link found:
    https://example.com/download1

    Press Enter to start the download...
    ```

3. **Download**:
    ```
    Download completed.
    ```

## Notes
- Ensure that you have `aria2c` installed and properly configured on your system.
- This script only filters out links from `readcomicsonline.ru` to ensure valid download links are shown.
- If no comics are found, try searching with a different keyword or adjusting the page number.

## License
This project is licensed under the MIT License.
