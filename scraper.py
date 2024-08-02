# scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd


class CovidDataScraper:
    def __init__(self, url):
        self.url = url
        self.page_content = None
        self.covid_table = None
        self.headers = []
        self.data = []

    def fetch_page_content(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                self.page_content = BeautifulSoup(response.content, "html.parser")
            else:
                print("Failed to retrieve data")
        except requests.RequestException as e:
            print(f"An error occurred while fetching the page: {e}")

    def extract_table(self):
        if self.page_content:
            self.covid_table = self.page_content.find("table", id="main_table_countries_today")
            if not self.covid_table:
                print("Table not found")
        else:
            print("Page content is empty")

    def extract_headers(self):
        if self.covid_table:
            header_row = self.covid_table.find("tr")
            self.headers = [th.text.strip() for th in header_row.find_all("th")]

    def extract_data(self):
        if self.covid_table:
            rows = self.covid_table.find_all("tr")[1:]  # Skip the header row
            for row in rows:
                row_data = [td.text.strip() for td in row.find_all("td")]
                self.data.append(row_data)

    def save_to_csv(self, file_name):
        if self.data and self.headers:
            df = pd.DataFrame(self.data, columns=self.headers)
            df.to_csv(file_name, index=False)
            print("Data saved to csv file")
        else:
            print("No data to save")

    def run(self, file_name):
        self.fetch_page_content()
        self.extract_table()
        self.extract_headers()
        self.extract_data()
        self.save_to_csv(file_name)