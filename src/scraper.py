from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time
import config as conf

def load_link(driver,url):

    """
        This function if used to open any link and make sur that it's fully loaded
    """

    # Following the link and waiting for the page to load
    driver.get(url)

    # Waiting for the page to fully load before starting the scraping
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    ) 
    # # Confirm
    # time.sleep(5)

    print(f"page opened: {driver.title}")


def extract_links_current(driver,url):

    """
        params : none
        For every page it extracts the links thant puts them into a list of links
        return : list of URLS
        works with : paginate - to itterate over all the pages
    """
    # # loading the current page
    # load_link(driver,url)


    # extract all links inside the div 
    links_elements = driver.find_elements(By.XPATH,"//div[contains(@class, 'sc-1nre5ec-1') and contains(@class, 'crKvIr') and contains(@class, 'listing')]//a")

    # using a comprehension list to store every href inside the hrefs list
    hrefs = [link.get_attribute('href') for link in links_elements]

    return hrefs


def paginate(driver,next_page): 

    # formating the link that i'll be working with
    link = f"{conf.website_URL}?o={next_page}"

    try:

        # searching for the div that noramlly contains all the listing
        driver.find_element(By.XPATH,'//*[@id="__next"]/div/main/div/div[5]/div[1]/div/div[1]')

        # if the element is found the page is loaded
        load_link(driver,link)
        print('Moving to the next page')

    except NoSuchElementException:

        # NoSuchElementException is where the element we're trying to find is not found.
        print('Oops, last page. The element was not found.')
    
    except Exception as e :
        # Handeling the other Exception that may arise.
        print(f'Error while moving to page {next_page}:', e)
        

    






    
def extract_links_all(driver,start_page,limit_pages,base_url):
    
    """
    params : none
    combines the extract_links_current and the paginate to extract all the available links
    return : the whole list of links to scrape
    """
    load_link(driver,f"{base_url}?o={start_page}")

    # This list will contain all the links 
    all_links = []
    # starting page link
    starting_url =  f"{base_url}?o={start_page}"
    current_page = start_page
    while current_page <= limit_pages:
        
        try :  
        
            links = extract_links_current(driver,f"{base_url}?o={current_page}")
            all_links.extend(links)
            paginate(driver,current_page + 1)
            current_page += 1

        except Exception as E : 

            print ("extracting links stoped : ",E)

    return all_links

    


    


def extract_listings_data(driver, listings_list):
    """
    Extracts and organizes data from each listing by:
    - Opening each listing URL and gathering specific data fields.
    - Appending data in a structured way to a main data list.
    
    Parameters:
        driver : Selenium WebDriver instance used to interact with browser.
        listings_list : List of URLs for each listing to extract data from.

    Returns:
        data_all : A list containing data dictionaries for each listing.
    """
    data_all = []  # Holds all listings data
    
    for listing in listings_list:
        current_listings = {}  # Dictionary for individual listing

        # Open the listing link
        load_link(driver, listing)

        # Extract title
        try:
            current_listings['title'] = driver.find_element(
                By.XPATH, '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/h1'
            ).text
        except NoSuchElementException:
            current_listings['title'] = None

        # Extract price
        try:
            current_listings['price'] = driver.find_element(
                By.XPATH, '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/p'
            ).text
        except NoSuchElementException:
            current_listings['price'] = None

        # Extract city
        try:
            current_listings['city'] = driver.find_element(
                By.XPATH, '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/span[1]'
            ).text
        except NoSuchElementException:
            current_listings['city'] = None

        # Extract timestamp
        try:
            time_element = driver.find_element(
                By.XPATH, '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/span[2]/time'
            )
            current_listings['datetime'] = time_element.get_attribute('datetime')
        except NoSuchElementException:
            current_listings['datetime'] = None

        # Extract additional info (rooms, baths, surface area)
        try:
            div_container = driver.find_element(
                By.XPATH, '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[4]/div[1]'
            )
            spans = div_container.find_elements(By.TAG_NAME, 'span')
            current_listings['nb_rooms'] = spans[0].text if len(spans) > 0 else None
            current_listings['nb_baths'] = spans[1].text if len(spans) > 1 else None
            current_listings['surface_area'] = spans[2].text if len(spans) > 2 else None
        except NoSuchElementException:
            current_listings['nb_rooms'] = current_listings['nb_baths'] = current_listings['surface_area'] = None


        # Not working to fix
        # Extract extra information into a dictionary
        try:
            cont_div = driver.find_element(
                By.XPATH, '//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[6]/div'
            )
            spans = cont_div.find_elements(By.TAG_NAME, 'span')
            
            # the logic is now to store data as a strings that groups the list of additional equipemment available
            for i in range(0, len(spans), 2):

                if i + 1 < len(spans):
                    
                    current_listings.setdefault("equipement",[]).append(spans[i].text)

            current_listings['equipement'] = ", ".join(current_listings['equipement'])
        
        except NoSuchElementException:
            current_listings['equipement'] = None


        

        # Add the current listing's data to the main list
        data_all.append(current_listings)


    return data_all
        




        

        
        
        





        
