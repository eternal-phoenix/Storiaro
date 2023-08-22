import load_django
from parser_app.models import ItemInfo, ItemLink
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep



class StoriaroParser:

    def __init__(self):
        self.DEBUG = True
        chrome_options = Options()
        service = Service(executable_path=os.path.abspath('chromedriver'))
        # chrome_options.add_argument("--window-size=500,1200")
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--enable-javascript')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--lang=en')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        
        self.find = self.driver.find_element
        self.finds = self.driver.find_elements


    def get_pagen(self) -> int:
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #scroll
        try:
            last_page = self.find(by=By.XPATH, value='//nav[@data-cy="pagination"]//button[5]')
            return int(last_page.text.strip())
        except (NoSuchElementException, ValueError):
            print('[INFO] no pagination available...')
            return False


    def collect_links(self, url: str) -> None:
        self.driver.get(url)
        # sleep(2)
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #scroll
        # sleep(2)

        links_items = self.finds(by=By.XPATH, value='//a[@data-cy="listing-item-link"]')
        links = [item.get_attribute('href') for item in links_items]
        if self.DEBUG:
            print(len(links))        
        
        for item, link in zip(links_items, links):
            name = item.find_element(by=By.XPATH, value='.//h3[@data-cy="listing-item-title"]').text.strip()
            if self.DEBUG:
                print(name, '########', link)

            defaults = {
                'name': name,
            }
            obj, created = ItemLink.objects.get_or_create(link=link, defaults=defaults)


    def get_item_info(self, item: ItemLink) -> None:
        name = item.name
        link = item.link
        print(link)

        self.driver.get(link)
        try:
            price = float(self.find(by=By.XPATH, value='//strong[@data-cy="adPageHeaderPrice"]').text.strip()[:-1].replace(' ', ''))
        except (NoSuchElementException, ValueError):
            price = None

        try:
            price_m2 = float(self.find(by=By.XPATH, value='//div[@aria-label="Prețul pe metru pătrat"] ').text.strip()[:-4].replace(' ', ''))
        except (NoSuchElementException, ValueError):
            price_m2 = None

        try:
            location = self.find(by=By.XPATH, value='//a[@aria-label="Abordare"]').text.strip()
        except (NoSuchElementException, ValueError):
            location = None

        try:
            surface = self.finds(by=By.XPATH, value='//div[@aria-label="Suprafață"]//div')[-1].text.strip()
            print(surface)
        except (NoSuchElementException, ValueError):
            surface = None

        try:
            rooms = self.finds(by=By.XPATH, value='//div[@aria-label="Numărul de camere"]//div')[-1].text.strip()
        except (NoSuchElementException, ValueError):
            rooms = None

        try:
            floor = self.finds(by=By.XPATH, value='//div[@aria-label="Etaj"]//div')[-1].text.strip()
        except (NoSuchElementException, ValueError):
            floor = None

        try:
            description = self.find(by=By.XPATH, value='//div[@data-cy="adPageAdDescription"]').text.strip().replace('\n', ' ')
        except (NoSuchElementException, ValueError):
            description = None

            

        defaults = {
            'name': name,
            'price': price,
            'price_m2': price_m2,
            'location': location,
            'surface': surface,
            'rooms': rooms, 
            'floor': floor,
            'description': description,
        }
        obj, created = ItemInfo.objects.get_or_create(link=link, defaults=defaults)

        if self.DEBUG:
            filler = '#################################'
            print(filler, link, name, price, price_m2, location, surface, rooms, floor, description, sep='\n')
