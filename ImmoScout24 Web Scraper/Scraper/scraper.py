from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import xml.etree.ElementTree as ET
import time
from datetime import datetime
import logging

from database import check_listing_exists, insert_listing, create_connection, create_table
from utils import format_address, notify_user_to_solve_captcha, convert_list_to_string


class ImmoScout24Scraper:
    def __init__(self, base_url, search_path, output_path):
        self.base_url = base_url
        self.search_path = search_path
        self.output_path = output_path

        chrome_options = Options()
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
    def start_browser(self):
        """ Initialize the browser and open the search page. """
        logging.info(f"Script started")

        self.driver.get(self.base_url + self.search_path)
        time.sleep(5)  # Adjust as needed for page load

    def close_browser(self):
        """ Close the browser. """
        logging.info(f"Browser closed")
        self.driver.quit()

    def solve_captcha(self):
        """ Prompt user to solve CAPTCHA if present. """
        notify_user_to_solve_captcha()

    def extract_listings(self, conn):
        """ Extract listings from the current page and handle pagination. """
        listings = []
        page_number = 0
                    
        # Get current date
        extraction_date = datetime.now().strftime("%Y-%m-%d")

        while True:
            page_number += 1
            listing_elements = self.driver.find_elements(By.CLASS_NAME, "result-list__listing")

            for element in listing_elements:
                try:
                    data_id = element.get_attribute('data-id')
                    title = element.find_element(By.CSS_SELECTOR, 'h2.result-list-entry__brand-title').text
                    # Remove "NEU" if it's in the title
                    title = title.replace("NEU", "").strip()
                    address = format_address(element.find_element(By.CSS_SELECTOR, 'div.result-list-entry__address').text)
                    expose_url_element = element.find_element(By.CSS_SELECTOR, 'div.result-list-entry__data a[href]')
                    expose_url = expose_url_element.get_attribute('href')

                    # Extract living space, rooms
                    living_space = rooms = None
                    criteria_elements = element.find_elements(By.CSS_SELECTOR, 'dl.result-list-entry__primary-criterion')

                    for criteria in criteria_elements:
                        label = criteria.find_element(By.TAG_NAME, 'dt').text.strip()
                        value = criteria.find_element(By.TAG_NAME, 'dd').text.strip()

                        if 'Kaltmiete' in label:
                            kaltmiete = value.replace(' €', '').replace('.', '').replace(',', '.') # Remove ' €'
                            kaltmiete = float(kaltmiete)
                        elif 'Wohnfläche' in label:
                            living_space = value.replace(' m²', '').replace(',', '.') # Remove ' m²'
                            living_space = float(living_space)
                        elif 'Zi.' in label:
                            rooms = value.replace(',', '.')
                            rooms = float(rooms)

                    # Extract secondary criteria
                    secondary_criteria_list = []
                    secondary_criteria_ul = element.find_elements(By.CSS_SELECTOR, 'ul.result-list-entry__secondary-criteria')
                    if secondary_criteria_ul:
                        secondary_criteria_items = secondary_criteria_ul[0].find_elements(By.TAG_NAME, 'li')
                        for item in secondary_criteria_items:
                            criteria_text = item.text.strip()
                            if criteria_text != "...":  # Exclude unspecified criteria
                                secondary_criteria_list.append(criteria_text)

                    secondary_criteria_str = convert_list_to_string(secondary_criteria_list)

                    # Append extracted data to listings
                    listings.append({
                        'data_id': data_id,
                        'title': title,
                        'address': address,
                        'kaltmiete': kaltmiete,
                        'living_space': living_space,
                        'rooms': rooms,
                        'secondary_criteria': secondary_criteria_str,
                        'url': expose_url
                    })

                    # Check if the listing already exists
                    if not check_listing_exists(conn, data_id, extraction_date):
                        # Insert into the database
                        listing = (data_id, title, address, kaltmiete, living_space, rooms, secondary_criteria_str, extraction_date, expose_url)
                        insert_listing(conn, listing)

                except Exception as e:
                    logging.error(f"Error extracting data from listing: {e}")

            # Check if there is a next page
            try:
                next_page_button = self.driver.find_element(By.CSS_SELECTOR, "li.p-next:not(.disabled) a[aria-label='Next page']")
                if next_page_button:
                    next_page_button.click()
                    time.sleep(5)  # Wait for the next page to load
                else:
                    break  # Exit the loop if no more pages
            except Exception as e:
                logging.error(f"Pagination error: {e}")
                break

        logging.info(f"Script ended")
        return listings

    def run(self):
        """ Run the scraper. """
        conn = None
        try:
            self.start_browser()
            self.solve_captcha()

            # Establish database connection
            conn = create_connection(self.output_path)
            if conn is not None:
                create_table(conn)

            listings = self.extract_listings(conn)  # Pass the connection to the extraction method
            return listings
        finally:
            self.close_browser()
            if conn:
                conn.close()
            logging.info(f"Database connection closed")


if __name__ == "__main__":
    # Load and parse the XML configuration file
    tree = ET.parse('config.xml')
    root = tree.getroot()

    # Extract configuration variables
    BASE_URL = root.find('base_url').text
    LOG_PATH = root.find('log_path').text
    OUTPUT_PATH = root.find('output_path').text
    rooms = root.find('rooms').text
    price = root.find('price').text
    livingspace = root.find('livingspace').text

    # Construct the search path#
    # specific search
    # SEARCH_PATH = f"/Suche/de/baden-wuerttemberg/ulm/wohnung-mieten?numberofrooms={rooms}&price={price}&livingspace={livingspace}&pricetype=rentpermonth&enteredFrom=result_list"
    # broad search
    SEARCH_PATH = f"/Suche/de/baden-wuerttemberg/ulm/wohnung-mieten"

    # Configure logging to include timestamp
    logging.basicConfig(filename=LOG_PATH,
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    scraper = ImmoScout24Scraper(BASE_URL, SEARCH_PATH, OUTPUT_PATH)
    scraped_data = scraper.run()
    print(scraped_data)