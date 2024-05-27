import requests
from bs4 import BeautifulSoup
import csv

class BaseCrawler:
    def __init__(self, url, output_file):
        self.url = url
        self.output_file = output_file
        self.soup = None

    def fetch(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.content, 'html.parser')
        else:
            raise Exception(f"Failed to fetch {self.url}. Status code: {response.status_code}")

    def parse(self):
        raise NotImplementedError("Subclasses should implement this method")

    def save_to_csv(self, data, headers):
        with open(self.output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)


class Formula1Crawler(BaseCrawler):
    def parse(self):
        table = self.soup.find('table', class_='resultsarchive-table')
        rows = table.find_all('tr')
        data = []

        for row in rows:
            columns = row.find_all('td')
            if columns:
                pos = columns[1].text.strip()
                driver_name = columns[2].text.strip().split('\n')
                driver_name = ' '.join(driver_name[:-1])
                nationality = columns[3].text.strip()
                car = columns[4].text.strip()
                pts = columns[5].text.strip()

                data.append([pos, driver_name, nationality, car, pts])

        headers = ['Position', 'Driver', 'Nationality', 'Car', 'Points']
        self.save_to_csv(data, headers)

class CS2ServerCrawler(BaseCrawler):
    def parse(self):
        servers_list = self.soup.find('div', id='gameserversListBox')
        data = []

        if servers_list:
            server_boxes = servers_list.find_all('div', class_='serverBox')
            for server_box in server_boxes:
                # Tên server
                server_name = server_box.find('a').text.strip()

                # Số người hiện tại
                player_count = server_box.find('div', class_='py-3 sm:py-2.5 text-right xl:pr-10 z-20').text.strip()

                # Địa chỉ IP
                ip_address = server_box.find('div', class_='basis-2/3 z-30').text.strip()

                # Tên map
                map_name = server_box.find('div', class_='py-3 text-right pr-4 truncate overflow-hidden').text.strip()

                # Số PING
                ping = server_box.find('div', id=lambda x: x and x.startswith('tooltipPing')).text.strip()

                data.append([server_name, player_count, ip_address, map_name, ping])

            headers = ['Server name', 'Players', 'IP', 'Map', 'Ping']
            self.save_to_csv(data, headers)

def get_crawler(url, output_file):
    if "formula1.com" in url:
        return Formula1Crawler(url, output_file)
    elif "cs2browser.com" in url:
        return CS2ServerCrawler(url,output_file)
    else:
        raise ValueError("No crawler available for this website")


# url = 'https://www.formula1.com/en/results.html/2024/drivers.html'
url = 'https://cs2browser.com/gamemode/zombie-escape/?max_ping=0'
output_file = 'drivers_list.csv'

crawler = get_crawler(url, output_file)
crawler.fetch()
crawler.parse()
