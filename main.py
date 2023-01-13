from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests

form_link = 'https://forms.gle/5HMoiNMvmdMrmGCK6'
house_link = 'https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.58610762548828%2C%22east%22%3A-122.28055037451172%2C%22south%22%3A37.66503360680628%2C%22north%22%3A37.88538511109395%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'
headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
           'Accept-Language': "el-GR,el;q=0.9",
           'Connection': "keep-alive"}


# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
def find_houses():
    """ It finds the houses as a list. Returns a list of html code"""
    response = requests.get(url=house_link, headers=headers).text
    soup = BeautifulSoup(response, "lxml")
    houses_list = soup.find(name="ul",
                            class_="List-c11n-8-81-1__sc-1smrmqp-0 srp__sc-1psn8tk-0 dXyjtp photo-cards with_constellation")
    houses = houses_list.find_all(name="div",
                                  class_="StyledPropertyCardDataWrapper-c11n-8-81-1__sc-1omp4c3-0 fEStTH property-card-data")
    return houses

find_houses()