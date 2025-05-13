from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from time import sleep

from bs4 import BeautifulSoup
import json

def read_data_from_web():

    # Step 1: Set up selenium options
    options = Options()
    options.add_argument("--headless")  # optional, for no GUI
    options.add_argument("--disable-gpu")

    # Step 2: Open the site with selenium
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    print("Loading site...")
    driver.get("https://air.sviva.gov.il")
    sleep(10)
    # Optional: wait for the site to fully load
    driver.implicitly_wait(10)

    # get time
    now = datetime.now()

    one_hour_frw = now + timedelta(hours=1)
    one_hour_frw = one_hour_frw.replace(minute=0, second=0, microsecond=0)
    to_string = one_hour_frw.strftime("%Y-%m-%d") + 'T' + one_hour_frw.strftime("%H:%M:%S")

    one_hour_ago = now - timedelta(hours=2)
    one_hour_ago = one_hour_ago.replace(minute=0, second=0, microsecond=0)
    from_string = one_hour_ago.strftime("%Y-%m-%d") + 'T' + one_hour_ago.strftime("%H:%M:%S")

    # URL of the API endpoint
    url = 'https://air-api.sviva.gov.il/v1/envista/stations/567/Average?from=' + from_string + '&to=' + to_string + '&fromTimebase=5&toTimebase=5&timeBeginning=false&useBackWard=true&includeSummary=false&roundType=1&unitid=-1&onlySummary=false&unitConversion=true&extendedAvgCalculations=false'

    driver.get(url)
    sleep(15)

    # Print raw response from the body
    print(driver.page_source)
    html = driver.page_source
    driver.quit()

    return html

def parse_html_to_list(html):

    soup = BeautifulSoup(html, 'html.parser')
    pre = soup.find('pre')

    # Extract text content (raw JSON)
    if pre:
        raw_json = pre.text
        data = json.loads(raw_json)
    else:
        data = {}

    return data