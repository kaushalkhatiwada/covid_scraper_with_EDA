# main.py

from scraper import CovidDataScraper

def main():
    URL = "https://www.worldometers.info/coronavirus/"
    scraper = CovidDataScraper(URL)
    scraper.run('covid_data.csv')

if __name__ == "__main__":
    main()