import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
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


def find_houses(page_source=None) -> (list, list, list):
    """Returns a Dictionary of All the Addresses, Prices, and Links
     address: List of Addreses,
     price: List of Prices,
     link: List of Links
     You can provide a custom page source, if not, it will find it's own through the Links HardCoded
    """
    if page_source is None:  # If page_source is not provided, will find it's own
        # The session variable is for retrying after failing to establishing connection
        # If request sessions will be applied periodicaly
        # Link: https://stackoverflow.com/a/47475019
        print("Page Source NOT provided, calculating it's own")
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
        print("Page Source Provided, Continue with that")
        soup = BeautifulSoup(page_source, "html.parser")

    all_link_elements = soup.select("#grid-search-results ul li article div div a"
                                    ".StyledPropertyCardDataArea-c11n-8-81-1__sc-yipmu-0")
    all_links = []
    for link in all_link_elements:
        href = link["href"]
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
            price = element.select("span")[0].get_text().replace("$", "").replace("+", "").replace("/", " ").split()[0]
        except IndexError:
            print('Multiple listings for the card')
            # Price with multiple listings
            price = element.select("li")[0].get_text().replace("$", "").replace("+", "").replace("/", " ").split()[0]
        finally:
            all_prices.append(price)
    return {"address": all_addresses,
            "price": all_prices,
            "link": all_links}


def fill_out_form(address_input: str, price_input: str, link_input: str):
    """
    It Fills out the google form with the provided info
    :return:
    """
    # Initial Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Go to Form Page
    driver.get(form_link)
    # Input information on the Google Form
    wait = WebDriverWait(driver, 10)  # Inital a WebDriverWait element to fill out the form
    address_form = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                                                                    '1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    address_form.send_keys(address_input)
    time.sleep(1)
    price_form = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                                                                  '2]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    price_form.send_keys(price_input)
    time.sleep(1)
    link_form = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                                                                 '3]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    link_form.send_keys(link_input)
    time.sleep(1)
    # Press the Submit Button
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div['
                                                                     '1]/div/span/span')))
    submit_button.click()
    time.sleep(1)
    # Refresh
    driver.get(form_link)
    time.sleep(1)


# MAIN
info = find_houses()
addresses = info["address"]
prices = info["price"]
links = info["link"]
for index in range(len(addresses)):  # Either addresses or prices or links, has the same length
    address = addresses[index]
    print(address)
    price = prices[index]
    print(price)
    link = links[index]
    print(link)
    fill_out_form(address_input=address,
                  price_input=price,
                  link_input=link)
