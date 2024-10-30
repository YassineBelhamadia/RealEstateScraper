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
    WebDriverWait(driver, 3).until(
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

    


    
def extract_listings_data(driver,listings_list):

    """
        - Combines all the functions listed above to extract the wanted data from each listing
        - fills a data structure with listings data in an organized way.
        

    """
    

    for listing in listings_list:

        # for each itteration we'll have a new one to store each lisiting
        current_listings = []

        # opening the listings link
        load_link(driver,listing)
        # click on the more details part to show all the info
        time.sleep(2)
        
        





        