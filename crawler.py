import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.formula1.com/en/results.html/2024/drivers.html'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='resultsarchive-table')
    rows = table.find_all('tr')

    with open('drivers_list.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Position', 'Driver', 'Nationality', 'Car', 'Points'])

        for row_id, row in enumerate(rows):
            columns = row.find_all('td')
            if columns:
                pos = columns[1].text.strip()
                driver_name = columns[2].text.strip().split('\n')
                driver_name = ' '.join(driver_name[:-1])
                nationality = columns[3].text.strip()
                car = columns[4].text.strip()
                pts = columns[5].text.strip()

                writer.writerow([pos, driver_name, nationality, car, pts])
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
