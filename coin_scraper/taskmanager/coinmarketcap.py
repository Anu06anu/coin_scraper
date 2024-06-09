import requests
from bs4 import BeautifulSoup
import re

class CoinMarketCap:
    BASE_URL = "https://coinmarketcap.com/currencies/"

    def __init__(self, coin):
        self.coin = coin

    def scrape(self):
        url = f"{self.BASE_URL}{self.coin}/"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.content, 'html.parser')
        return self.parse_data(soup)

    def parse_data(self, soup):
        data = {}
        data['price'] = self.get_price(soup)
        data['price_change'] = self.get_price_change(soup)
        data['market_cap'] = self.get_market_cap(soup)
        data['extract_data'] = self.get_extract_data(soup)
        data['contracts'] = self.get_contracts(soup)
        data['official_links'] = self.get_official_links(soup)
        data['socials'] = self.get_socials(soup)
        return data

    def get_price(self, soup):
        price_tag = soup.find('span', class_='sc-d1ede7e3-0 fsQm base-text')
        if price_tag:
            return price_tag.text
        return None

    def get_price_change(self, soup):
        change_tag = soup.find('span', class_='sc-d1ede7e3-0 fsQm base-text')
        if change_tag:
            return change_tag.text
        return None

    def get_market_cap(self, soup):
        market = soup.find('dd').text
        market_cap = re.search(r'\$[\d,]+', market).group()
        return market_cap

    def get_extract_data(self, soup):
        show_text = soup.find(id="section-coin-stats")
        if not show_text:
            return {}
        
        show_text = show_text.text
        heading_pattern = r'[A-Za-z/]+(?: \(24h\))?'  # Matches headings with optional "(24h)" suffix
        number_pattern = r'\$?[\d,]+(?:\.\d+)?'  # Matches numbers with optional dollar sign and decimal part

        # Find all occurrences of headings and numbers in the text
        headings = re.findall(heading_pattern, show_text)
        numbers = re.findall(number_pattern, show_text)

        # Zip headings and numbers together
        data = zip(headings, numbers)

        # Store the data in a dictionary
        data_dict = {heading.strip(): number for heading, number in data}

        return data_dict

    def get_contracts(self, soup):
        a_tag = soup.find('a', class_='chain-name')
        if a_tag:
            # Extract name and address
            name = a_tag.find('span', class_='dEZnuB').text.strip().replace(':', '')
            address = a_tag.find('span', class_='eESYbg').text.strip()
            # Create a dictionary
            result = {"name": name, "address": address}
            return result
        return {}

    def get_official_links(self, soup):
        a_tags = soup.find_all('a', href=True)
        for a_tag in a_tags:
            if 'Website' in a_tag.get_text(strip=True):
                link = a_tag['href']
                name = a_tag.get_text(strip=True)
                result = {"name": name, "link": link}
                return result
        return {}

    def get_socials(self, soup):
        a_tags = soup.find_all('a', href=True)
        results = []
        for a_tag in a_tags:
            text = a_tag.get_text(strip=True).lower()
            if 'twitter' in text:
                results.append({"name": "twitter", "url": a_tag['href']})
            elif 'telegram' in text:
                results.append({"name": "telegram", "url": a_tag['href']})
        return results
