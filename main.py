from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests
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
def find_houses() -> [list, list, list]:
    """Returns a List of 3 Lists, index: per house.
     1. List of Addreses,
     2. List of Prices,
     3. List of Links
    """
    # The session variable is for retrying after failing to establishing connection
    # If request sessions will be applied periodicaly
    # Link: https://stackoverflow.com/a/47475019
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    # Getting the data
    response = session.get(url=house_link, headers=headers).text
    soup = BeautifulSoup(response, "lxml")
    # all_houses_list = soup.find(name="ul",
    #                             class_="List-c11n-8-81-1__sc-1smrmqp-0 srp__sc-1psn8tk-0 dXyjtp photo-cards with_constellation")
    # section_of_houses = all_houses_list.find_all(name="li",
    #                                              class_="ListItem-c11n-8-81-1__sc-10e22w8-0 srp__hpnp3q-0 enEXBq with_constellation")

    section_of_houses = soup.find_all(name="article", class_="StyledPropertyCard-c11n-8-81-1__sc-jvwq6q-0 gItDJf srp__sc-15y3msw-0 epgJFL property-card list-card_for-rent list-card_building list-card_not-saved")
    # Itterate per house to find informations
    # print(section_of_houses)
    print("**********\n\n\n********")
    list_of_links = []
    list_of_addresses = []
    list_of_prices = []
    for house in section_of_houses:
        try:  # Some times returns None Type and we get a NoneType Error
            info = house.find(name="div",
                          class_="StyledPropertyCardDataWrapper-c11n-8-81-1__sc-1omp4c3-0 fEStTH property-card-data")
            # Links
            link = info.find(name='a').get("href")
            print("**********\n\n\n********")
            if link.startswith("/b/"):  # It means we will get partial link
                # Add the rest link
                html_links = "https://www.zillow.com/" + info.get("href")
                print(html_links)
                list_of_links.append(html_links)
            # Addresses
            address = info.find(name="address").getText()
            print(address)
            list_of_addresses.append(address)
            # Prices
            price = info.find(name="div", class_="StyledPropertyCardDataArea-c11n-8-81-1__sc-yipmu-0 wgiFT").getText()
            pprint(price)
            list_of_prices.append(price)

            return [list_of_addresses, list_of_prices, list_of_links]
        except:
            print("Continue..")
            continue


find_houses()
