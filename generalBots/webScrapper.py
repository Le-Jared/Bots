import argparse
from bs4 import BeautifulSoup
import requests
import csv
import os
import time
from fake_useragent import UserAgent

def scrape_website(url, proxies):
    headers = {
        "User-Agent": ua.random
    }
    r = requests.get(url, headers=headers, proxies=proxies)
    
    if r.status_code != 200:
        print(f"Failed to retrieve page. Status code: {r.status_code}")
        return None

    soup = BeautifulSoup(r.text, 'html.parser')
    
    return soup

def write_to_file(data, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def check_file_exists(filename):
    if not os.path.isfile(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Description"])

def clean_data(data):
    return ' '.join(data.split())

def main():
    parser = argparse.ArgumentParser(description='Scrape a website.')
    parser.add_argument('--url', type=str, help='The base URL to scrape')
    args = parser.parse_args()

    base_url = args.url
    filename = 'output.csv'
    check_file_exists(filename)
    
    proxies = {
        "http": "http://10.10.1.10:3128",
        "https": "http://10.10.1.10:1080",
    }

    ua = UserAgent()

    url = base_url
    while url is not None:
        soup = scrape_website(url, proxies)
        
        if soup is None:
            continue

        items = soup.find_all('div', attrs={'class': 'item'})

        for item in items:
            try:
                title = clean_data(item.find('h2').text)
                description = clean_data(item.find('p').text)
                
                write_to_file([title, description], filename)
                
            except Exception as e:
                print(f"Error when processing an item: {e}")

        next_page = soup.find('a', attrs={'class': 'next'})
        if next_page is None:
            break
        else:
            url = base_url + next_page.get('href')

        time.sleep(1)

if __name__ == "__main__":
    main()

