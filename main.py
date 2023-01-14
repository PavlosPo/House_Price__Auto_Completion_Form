import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests
import re  # Regex Spliting
from pprint import pprint
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

form_link = 'https://docs.google.com/forms/d/e/1FAIpQLSfgMr8OnmIkgczxtasHuvqEo7H0TTvMdL45ssw54UDd-_9avQ/viewform'
house_link = 'https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.58610762548828%2C%22east%22%3A-122.28055037451172%2C%22south%22%3A37.66503360680628%2C%22north%22%3A37.88538511109395%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    'Accept-Language': "el-GR,el;q=0.9",
    'Connection': "keep-alive"}


def find_houses(page_source=None) -> [list, list, list]:
    """Returns a List of 3 Lists, index: per house.
     1. List of Addreses,
     2. List of Prices,
     3. List of Links
     You can provide a custom page source, if not, it will find it's own through the Links HardCoded
    """
    if page_source is None:  # If page_source is not provided, will find it's own
        # The session variable is for retrying after failing to establishing connection
        # If request sessions will be applied periodicaly
        # Link: https://stackoverflow.com/a/47475019
        print("Page_Source Not provided, calculating it's own")
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        # Getting the data
        response = session.get(url=house_link, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    else:  # if page source is provided then continue with that
        print("Page Source Provided, continue with that")
        soup = BeautifulSoup(page_source, "html.parser")

    all_link_elements = soup.select("#grid-search-results ul li article div div a" 
                                    ".StyledPropertyCardDataArea-c11n-8-81-1__sc-yipmu-0")
    all_links = []
    for link in all_link_elements:
        href = link["href"]
        print(href)
        if "http" not in href:
            all_links.append(f"https://www.zillow.com{href}")
        else:
            all_links.append(href)

    all_address_elements = soup.select("#grid-search-results ul li article a address")
    all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]

    all_price_elements = soup.select("#grid-search-results ul li article")
    all_prices = []
    for element in all_price_elements:
        # Get the prices. Single and multiple listings have different tag & class structures
        try:
            # Price with only one listing
            price = element.select("span")[0].get_text()
        except IndexError:
            print('Multiple listings for the card')
            # Price with multiple listings
            price = element.select("li")[0].get_text()
        finally:
            all_prices.append(price)
    return [all_addresses, all_prices, all_links, (len(all_addresses), len(all_prices), len(all_links))]



#
# find_houses()
#
# # Selenium Section
# def fill_out_form():
#     # Initial Selenium
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     # Go to Form Page
#     driver.get(form_link)
#     # Retrieve informations from Houses
#     # [address, price, link] = find_houses()
#     forms_to_complete = [item.find_element(by=By.TAG_NAME, value="input") for item in driver.find_elements(by=By.CLASS_NAME, value="Xb9hP")]  # 3 questions -> 3 items in the list
#     # Input information on the Google Form
#     address_form = WebDriverWait(driver, 1012121).until(lambda driver: driver.find_element(by=By.CSS_SELECTOR, value='.ndJi5d .snByac')).click()
#     address_form.send_keys("aswdeq")
#     time.sleep(1)
#     price_form = forms_to_complete[1]
#     time.sleep(1)
#     link_form = forms_to_complete[2]
#     time.sleep(10)
#     print(address_form, price_form, link_form)
#     # Press the Submit Button
#     submit_button = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div['
#                                                             '1]/div/span/span')
#     submit_button.click()
#     time.sleep(1)
#     # Refresh
#     driver.get(form_link)
#
# # fill_out_form()
items = find_houses()
print(items[0], items[1], items[2], items[3])
