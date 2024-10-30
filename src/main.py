import chromedriver_autoinstaller  # Installs the chromedriver according the chrome version you have.
from selenium import webdriver
import config as conf
import scraper as sp
import data_processing

# Install the desired verison of chromedriver.
chromedriver_autoinstaller.install()
print("Chromedriver installed.")








def main():
    # initializing the chrome driver.
    driver = webdriver.Chrome()

    try : 


        
        first_four = []

        first_four = sp.extract_links_all(driver,3,4,conf.website_URL)
    
        sp.extract_listings_data(driver,first_four)
        

        



        


    finally : 
         
         # Closing the browser.
         driver.quit()

if __name__ == "__main__":
    main()