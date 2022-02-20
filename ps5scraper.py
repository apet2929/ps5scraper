from datetime import datetime
from json import JSONDecoder
import re
from time import sleep, time
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
from selenium.common.exceptions import TimeoutException
import logging
import multiprocessing
import requests

import undetected_chromedriver as uc 

class InStockException(Exception):
    pass

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
    # # options.add_argument("--incognito") #   Disables caching/
    # options.add_argument('--headless')  # Makes the window invisible

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

    options = uc.ChromeOptions()
    # options.add_argument("--incognito") #   Disables caching
    # options.add_argument('--headless')  # Makes the window invisible
    driver = uc.Chrome(desired_capabilities=d, options=options)
    
    print("Chromedriver initialization success!")
    # driver = selenium.webdriver.Chrome(resource_path("assets/chromedriver.exe"), options=options, desired_capabilities=d)
     
    driver.implicitly_wait(20)

    l = logging.getLogger('selenium.webdriver.remote.remote_connection')
    l.disabled = True
    # print("Disablling logger")

    return driver

def start(driver: Chrome):
    wait = WebDriverWait(driver, 20)
    driver.get("https://www.smythstoys.com/uk/en-gb/video-games-and-tablets/playstation-5/playstation-5-consoles/playstation-5-digital-edition-console/p/191430")
    wait.until(EC.title_is("PlayStation 5 Digital Edition Console | Smyths Toys UK"))


def check_blocked(driver):
    html = get_page_html(driver)
    if "Request unsuccessful." in html:
        write_output(html)
        return True
    return False


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

def do_request(headers, cookies, data):
    response = requests.post('https://www.smythstoys.com/uk/en-gb/store-pickup/191430/pointOfServices', headers=headers, cookies=cookies, data=data)

    write_output("request_response", response.text)
    return response
        
def parse_json(json):
    d = json["data"]

    # print(str(data))
    

    locationStatusList = []
    for i in range(len(d)):
        data = d[i]
        location = data["name"]
        status = data["stockLevelStatusCode"]
        locationStatusList.append((location, status))

    return locationStatusList

def get_CSRF_token(driver: Chrome):
    elem = driver.find_element(By.CSS_SELECTOR, "form.add_to_cart_form:nth-child(2) > div:nth-child(15) > input:nth-child(1)")
    assert elem.get_attribute("name") == "CSRFToken"
    return elem.get_attribute("value")

def get_request_data(driver: Chrome):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.smythstoys.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.smythstoys.com/uk/en-gb/video-games-and-tablets/playstation-5/playstation-5-consoles/playstation-5-digital-edition-console/p/191430',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    _cookies = driver.get_cookies()
    cookies = {}
    for cookie in _cookies:
        cookies[cookie["name"]] = cookie["value"]

    data = {
        'cartPage': 'false',
        'entryNumber': '0',
        'latitude': '',
        'longitude': '',
        'searchThroughGeoPointFirst': 'false',
        'xaaLandingStores': 'false',
        'CSRFToken': get_CSRF_token(driver)
    }
    return (headers, cookies, data)

def check_in_stock(locationStatusList, callback):
    
    for location, status in locationStatusList:
        if(status != "outOfStock"):
            callback(location, status)
            return True
    return False

def new_main():
    print("Setup begin")
    
    try:
        driver: Chrome = setup_selenium()
    except:
        driver: Chrome = setup_selenium()

    target_phone_numbers = [os.getenv("TEMP_PHONE_NUM"), os.getenv("TO_PHONE_NUM")]
    print("Setup complete")
    
    run = True
    while run:
        try:
            current_time = datetime.now()
            print(f"Starting, time = {str(current_time)} start time = {str(start_time)}")
            start(driver)
            if(check_blocked(driver)):
                print("We got blocked!")
                log_error_time(start_time, current_time)
                quit()
            
            continue_same_session = True
            while continue_same_session:
                print("Getting request data")
                headers, cookies, data = get_request_data(driver)
                write_output("request_data", f"{str(headers)}\n{str(cookies)}\n{str(data)}")
                print("Sending request")
                response = do_request(headers, cookies, data)
                
                continue_same_session = response.status_code == 200
                if response.status_code != 200:
                    print("We got blocked!")
                    print(response.status_code, response.text)
                    log_error_time(start_time, current_time)
                
                print("Parsing JSON")
                json = JSONDecoder().decode(response.text)
                locationStatusList = parse_json(json)
            

                def callback(name, stock):
                    if(stock != "outOfStock"):
                        print("Not out of stock!", stock)
                        send_texts(get_body(name, stock), target_phone_numbers)
                        raise InStockException(get_body(name, stock))
                print("Checking stock level")
                if not check_in_stock(locationStatusList, callback=callback):
                    print("None in stock")

                sleep(10)


        except KeyboardInterrupt as e:
            run = False
            quit()
        except InStockException as e:
            print(e)
            run = False
        except Exception as e:
            print(e)
            # Continue execution


def test():
    with open("request_response.txt", "r", encoding="utf-8") as response:
        json = JSONDecoder().decode(response.read())
    
    # parse_json(json)
    print(parse_json(json))
    quit()

def write_output(file_name, content):
    with open(f"{file_name}.txt", "w", encoding="utf-8") as file:
        file.write(content)

def log_error_time(start_time, end_time):
    with open("errorLog.txt", "a") as logFile:
        logFile.write(f"We got blocked! Start time = {str(start_time)} end time = {str(end_time)}")

if __name__ == "__main__":
    multiprocessing.freeze_support()

    start_time = datetime.now()

    try:
        load_dotenv()
        new_main()
    except Exception:
        import traceback
        traceback.print_exc()
        print("Program crashed; press Enter to exit")
