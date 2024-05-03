import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import pandas as pd



user_agents = [
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
]


# Get all city links from the main page
def get_city_links(start_url):
    """Get all city links from the main page."""
    city_links = []
    response = requests.get(start_url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        for div in soup.find_all('div', class_='itemlist'):
            a_tag = div.find('a')
            if a_tag and 'href' in a_tag.attrs:
                city_links.append(a_tag['href'])
    return city_links

# Get all address details from a city page
def get_addresses_from_city_page(city_url):
    """Get all address details from a city page."""
    addresses = []
    response = requests.get(city_url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        address_divs = soup.find_all('div', class_='address-left')
        for address_div in address_divs:
            try:
                store_name = address_div.find('a').get_text(strip=True)
                address_parts = [span.get_text(strip=True) for span in address_div.find_all('span')]
                store_address = f"{address_parts[1]}, {address_parts[2]}"
                zip_code = address_parts[-3]

                addresses.append({
                    'store_name': store_name,
                    'store_address': store_address,
                    'zip_code': zip_code,
                })
            except Exception as e:
                print(f"Error processing address: {e}")
    return addresses


start_url = "https://locations.traderjoes.com/ca/"
city_links = get_city_links(start_url)

all_addresses = []
for link in city_links:
    city_name = link.split('/')[-2]  
    full_link = urljoin(start_url, link)  
    city_addresses = get_addresses_from_city_page(full_link)  
    for address in city_addresses:
        address['city'] = city_name  
        all_addresses.append(address)  

for address in all_addresses:
    print(f"city: {address['city']}, store name: {address['store_name']}, store address: {address['store_address']} zip-code: {address['zip_code']}")


df = pd.DataFrame(all_addresses)
df['store_number'] = df['store_name'].str.extract(r'(\d+)')
df['store_name'] = df['store_name'].str.replace(r'\s*\(\d+\)', '').str.strip()  
df = df.drop(columns=['city'])
df
df.to_csv('trader_joes_locations.csv', index=False)


