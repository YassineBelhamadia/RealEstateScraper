import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import config as conf
import scraper as sp
import data_processing as csv
import logging
import time

# Install ChromeDriver
chromedriver_autoinstaller.install()
logging.info("Chromedriver installed.")

def main():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")  # Optional headless mode

    # Initialize Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Extract links with retries
        listings = []
        MAX_RETRIES = 3
        for attempt in range(MAX_RETRIES):
            try:
                listings = sp.extract_links_all(driver, 1, 40, conf.website_URL)
                break
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed with error: {e}")
                time.sleep(2)
        else:
            logging.error("Max retries reached. Exiting.")
            return
        
        # Process data
        data = sp.extract_listings_data(driver, listings)
        csv.data_to_csv(data)

    finally:
        # Quit driver
        driver.quit()

if __name__ == "__main__":
    logging.basicConfig(filename='scraper.log', level=logging.INFO, 
                        format='%(asctime)s:%(levelname)s:%(message)s')
    main()
