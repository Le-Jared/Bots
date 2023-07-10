from bs4 import BeautifulSoup
import requests
import csv
import os
import time

def scrape_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    
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
    base_url = "http://example.com"  # replace with the url you want to scrape
    filename = 'output.csv'
    check_file_exists(filename)
    
    for i in range(1, 6):  # adjust range according to the number of pages you want to scrape
        url = f"{base_url}/page/{i}"  
        soup = scrape_website(url)
        
        if soup is None:
            continue

        # Assume each page has multiple items wrapped in div tags with class 'item'
        items = soup.find_all('div', attrs={'class': 'item'})

        for item in items:
            try:
                # Assume each item has a 'title' in a h2 tag and 'description' in a p tag
                title = clean_data(item.find('h2').text)
                description = clean_data(item.find('p').text)
                
                # Write the data to a CSV file
                write_to_file([title, description], filename)
                
            except Exception as e:
                print(f"Error when processing an item: {e}")
        
        # Delay between requests
        time.sleep(1)

if __name__ == "__main__":
    main()

