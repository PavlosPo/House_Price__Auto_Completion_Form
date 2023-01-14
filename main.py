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

form_link = 'https://forms.gle/5HMoiNMvmdMrmGCK6'
house_link = 'https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.58610762548828%2C%22east%22%3A-122.28055037451172%2C%22south%22%3A37.66503360680628%2C%22north%22%3A37.88538511109395%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    'Accept-Language': "el-GR,el;q=0.9",
    'Connection': "keep-alive"}


# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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
        soup = BeautifulSoup(response.text, "lxml")
    else:  # if page source is provided then continue with that
        print("Page Source Provided, continue with that")
        soup = BeautifulSoup(markup=page_source, parser="lxml")

    # Starting the scrapping
    result_page = soup.find(name="ul",
                            class_="List-c11n-8-81-1__sc-1smrmqp-0 srp__sc-1psn8tk-0 dXyjtp photo-cards "
                                   "with_constellation")  # Here loads the results
    section_of_houses = result_page.find_all(name="li")  # here we go on each house section
    print("len of section of houses:", len(section_of_houses))
    # Itterate per house to find informations
    print("********** Start ********")
    pprint(section_of_houses)
    list_of_links = []
    list_of_addresses = []
    list_of_prices = []
    for house in section_of_houses:  # itterate through the houses
        try:  # Some times returns None Type and we get a NoneType Error
            # Links
            link = house.find(name="a",
                              class_="StyledPropertyCardDataArea-c11n-8-81-1__sc-yipmu-0 lpqUkW property-card-link").get(
                "href")
            print("********** Link Section ********")
            if link.startswith("/b/"):  # It means we will get partial link
                # Add the rest link
                link = "https://www.zillow.com/" + link
                list_of_links.append(link)
            print(link)
            # Addresses
            address = house.find(name="address").getText()
            print("********** Address Section ********")
            print(address)
            list_of_addresses.append(address)
            # Prices
            price = house.find(name="div",
                               class_="StyledPropertyCardDataArea-c11n-8-81-1__sc-yipmu-0 wgiFT").span.getText()
            price = price.replace("$", "").replace("+", "").split()[0]
            print("********** Price Section ********")
            print(price)
            list_of_prices.append(price)
        except:
            print("Skipped because of an Error..\n")
            continue
    # Return the Lists after all
    return [list_of_addresses, list_of_prices, list_of_links]


find_houses()