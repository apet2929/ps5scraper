import re
from time import sleep
import os
from twilio.rest import Client
from dotenv import load_dotenv 
import selenium
import sys
import selenium.webdriver.support.expected_conditions as EC
from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium.common.exceptions import *
from selenium.webdriver import Chrome
import selenium.webdriver.common.service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
import logging
import multiprocessing

import undetected_chromedriver as uc 


def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def setup_selenium() -> selenium.webdriver.Chrome:
    # # Options
    # options = selenium.webdriver.ChromeOptions()
    # # options.add_argument("--incognito") #   Disables caching
    # # options.add_argument('--headless')  # Makes the window invisible

    # # Disable logging            
    # options.add_argument("--log-level=OFF")
    # options.add_argument('--disable-gpu')   
    # options.add_argument("--disable-logging")
    # options.add_argument("--output=/dev/null");
    # options.add_argument("--disable-dev-shm-usage");

    # # Makes it work on other machines
    # sw_options = {
    #     # "request-storage": "memory",
    #     'request_storage_base_dir': resource_path("assets")
    # }

    # Capabilities
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'browser': 'ALL'}
    print("Initializing Chromedriver")

    driver = uc.Chrome(desired_capabilities=d)
    
    print("Chromedriver initialization success!")
    # driver = selenium.webdriver.Chrome(resource_path("assets/chromedriver.exe"), options=options, desired_capabilities=d)
     
    driver.implicitly_wait(20)

    l = logging.getLogger('selenium.webdriver.remote.remote_connection')
    l.disabled = True
    # print("Disablling logger")

    return driver

def start(driver: Chrome):
    driver.get("https://www.smythstoys.com/uk/en-gb/video-games-and-tablets/playstation-5/playstation-5-consoles/playstation-5-digital-edition-console/p/191430")
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cookieProcessed")))
        elem = driver.find_element(By.CSS_SELECTOR,".cookieProcessed")
        elem.click()
    except:
        regain_focus(elem)
        pass

def regain_focus(element):
    element.find_element_by_xpath("./ancestor::div[@class='row']").click()

def refresh(driver: Chrome):
    driver.refresh()
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#product_191430")))
    except:
        driver.refresh()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#product_191430")))

    trying = True

    while trying:
        try:
            print("Trying to click on 'List stores' button")
            elem = driver.find_element(By.CSS_SELECTOR,"#product_191430")
            elem.click()
            print("Button clicked, finding table")
        except:
            regain_focus(elem)
        try:
            elem = driver.find_element(By.XPATH ,"/html/body/div[11]/div[1]/div[2]/div[2]/div[1]/div/div/div/div[1]/div/div/div[3]/ul")
            trying = False
        except:
            regain_focus(elem)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.pickup-store-list-entry:nth-child(1)")))
    except:
        regain_focus(elem)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.pickup-store-list-entry:nth-child(1)")))

    html = get_page_html(driver)
    return html

def get_page_html(driver):
    # TODO : Figure out why this sometimes messes up
    elem = driver.find_element(By.XPATH, "//*")
    return elem.get_attribute("outerHTML")

def send_texts(text_body, phone_nums):
    SSID = os.getenv("SSID")
    AUTH_TOKEN = os.getenv("AUTH_TOKEN")
    MY_PHONE_NUM = os.getenv("MY_PHONE_NUM")
    client = Client(SSID, AUTH_TOKEN)
    for num in phone_nums:
        client.messages.create(
            to=num,
            from_=MY_PHONE_NUM,
            body=text_body
        )

def get_body(location_name, stock_level):
    return f'The PS5 is available in {location_name}! The stock level is: {stock_level}'


def get_html_from_file():
    with open("page.html", "r", encoding="utf-8") as saved:
        html = saved.read()
    return html

def get_data_from_html(html, callback_function):
    soup = BeautifulSoup(html, "html.parser")
    locations = list(soup.find_all(class_="pickup-store-list-entry"))
    for location in locations:
        name, stock = get_location_data(location)
        callback_function(name, stock)

def get_location_data(location):
    name = location.find(class_="pickup-store-list-entry-name")
    stock = location.find(class_="resultStock")

    return (strip_stuff(name.text).strip(), strip_stuff(stock.text).strip())

def strip_stuff(string):
    return re.sub('\s+',' ',string)

def main():    
    print("Setup begin")
    driver = setup_selenium()
    target_phone_numbers = [os.getenv("TEMP_PHONE_NUM"), os.getenv("TO_PHONE_NUM")]
    print("Setup complete")
    
    start(driver)
    while True:
        print("Checking for stock availability")
        html = refresh(driver)

        def callback(name, stock):
            if(stock != "Out Of Stock"):
                print("Not out of stock!", stock)
                send_texts(get_body(name, stock), target_phone_numbers)
                quit()
                
        get_data_from_html(html, callback_function=callback)
        print("None in stock\n")
        sleep(3)
        
def test():
    with open("page.html", "r", encoding="utf-8") as page:
        html = page.read()
    def callback(name, stock):
        if(stock != "Out Of Stock"):
            print("Not out of stock!", stock, name)

    get_data_from_html(html, callback_function=callback)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    load_dotenv()

    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        print("Program crashed; press Enter to exit")
