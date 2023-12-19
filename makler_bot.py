import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

LINK_G_FORM = 'https://forms.gle/U4SiXNEcLerdCt8XA'

service = ChromeService(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)


def render_page(url):
    driver.get(url)
    time.sleep(3)
    r = driver.page_source
    return r


class Bot:

    def __init__(self):
        self.r = render_page('https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56825484228516%2C%22east%22%3A-122.29840315771484%2C%22south%22%3A37.69125507932882%2C%22north%22%3A37.85923241333961%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D')
        self.soup = BeautifulSoup(self.r, 'html.parser')
        self.links = []
        self.scan()

    def scan(self):
        buffer = self.soup.find(id='grid-search-results')
        property_list = buffer.find_all_next(class_=re.compile('jVBMsP'))
        for result in property_list:
            address = result.find_next('address').text
            if result.find_next('a')['href'][0] == 'h':
                link = result.find_next('a')['href']
            else:
                link = f"https://www.zillow.com/{result.find_next('a')['href']}"
            price = result.find_next(class_=re.compile('bqsBln')).text
            self.links.append((address, price, link))
        print(len(self.links))
        return None

    def fill_table(self):
        for property in self.links:
            driver.get(LINK_G_FORM)
            time.sleep(0.5)
            address_input = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            address_input.send_keys(property[0])
            price_input = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price_input.send_keys(property[1])
            link_input = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link_input.send_keys(property[2])
            send_btn = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div')
            send_btn.click()
            next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            next_btn.click()
