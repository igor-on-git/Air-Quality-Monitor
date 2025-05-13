from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from time import sleep
from datetime import datetime, timedelta

CHROMEDRIVER_PATH = 'C:/Users/FileServer/ChromeDriver'

# Step 1: Set up selenium options
options = Options()
options.add_argument("--headless")  # optional, for no GUI
options.add_argument("--disable-gpu")

# Step 2: Open the site with selenium
#service = Service(CHROMEDRIVER_PATH)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

print("Loading site...")
driver.get("https://air.sviva.gov.il")
sleep(5)
# Optional: wait for the site to fully load
driver.implicitly_wait(10)

# Step 3: Extract cookies
selenium_cookies = driver.get_cookies()
#driver.quit()

# Convert to a format usable by requests
cookies_all = {cookie['name']: cookie['value'] for cookie in selenium_cookies}


verification_token = cookies_all.get('__RequestVerificationToken')
cookies = {
    'X-Access-Token': cookies_all['__FormVerificationToken'] + '; _ga=' + cookies_all['_ga'] + '; _ga_WGE8CEE6C3=' + cookies_all['_ga_WGE8CEE6C3'],
}

# thresholds
thresholds = {}
thresholds['NO'] = 10

# get time
now = datetime.now()

one_hour_frw = now + timedelta(hours=1)
one_hour_frw = one_hour_frw.replace(minute=0, second=0, microsecond=0)
to_string = one_hour_frw.strftime("%Y-%m-%d") + 'T' + one_hour_frw.strftime("%H:%M:%S")

one_hour_ago = now - timedelta(hours=1)
one_hour_ago = one_hour_ago.replace(minute=0, second=0, microsecond=0)
from_string = one_hour_ago.strftime("%Y-%m-%d") + 'T' + one_hour_ago.strftime("%H:%M:%S")

# Start a session to persist cookies
session = requests.Session()

# 1. Load the main page to get cookies and tokens
homepage_url = 'https://air.sviva.gov.il'
response = session.get(homepage_url, headers={
    'User-Agent': 'Mozilla/5.0',
})

# create request

# URL of the API endpoint
url = 'https://air-api.sviva.gov.il/v1/envista/stations/567/Average?from=' + from_string +'&to=' + to_string + '&fromTimebase=5&toTimebase=5&timeBeginning=false&useBackWard=true&includeSummary=false&roundType=1&unitid=-1&onlySummary=false&unitConversion=true&extendedAvgCalculations=false'

driver.get(url)
# Print raw response from the body
print(driver.page_source)
temp = driver.page_source
driver.quit()

# Headers copied from cURL
headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'access-control-allow-credentials': 'true',
    'access-control-allow-origin': 'https://air.sviva.gov.il',
    'authorization': 'JwtToken',
    'compression': 'gzip',
    'content-type': 'application/json; charset=utf-8',
    'contentlength': '0',
    'domainname': 'sviva',
    'envi-data-source': 'MANA',
    'origin': 'https://air.sviva.gov.il',
    'priority': 'u=1, i',
    'referer': 'https://air.sviva.gov.il/',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    #'x-requestverificationtoken': verification_token,
    'x-requestverificationtoken': '4wIpooDoAjrbFrMDxxiAnJG0wt3qrm0EIgItts_-c0Xp9Ng0zsWlTDX6MbRs3AusMdwPghrRgpV89O14B6mLTMOBgNHPZWtNRUYE7zcEOc41',
}
''''''
# Cookies copied from cURL (if needed)
cookies2 = {
    'X-Access-Token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6Ikd1ZXN0IiwibmJmIjoxNzQ3MTU4NzE0LCJleHAiOjE3NDcxNjIzMTQsImlhdCI6MTc0NzE1ODcxNH0.Vk51AhzVBK5T-BLC00pYZAYv4gISOP7b4Cv62jSF2vA; _ga=GA1.1.1510370736.1747065284; _ga_WGE8CEE6C3=GS2.1.s1747158721$o2$g0$t1747158721$j0$l0$h0',
}
''''''
# Send GET request with headers and cookies
response = requests.get(url, headers=headers, cookies=cookies)
#response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON data
    print(data)  # Process the data as needed

    print(data['data'][-1]['datetime'][:10])
    print(data['data'][-1]['datetime'][11:16])

    channels = data['data'][-1]['channels']  # Assuming the data has a 'stations' key
    for channel in channels:
        if channel['valid']:
            name = channel['name']
            units = channel['units']
            value = channel['value']
            print(f"{name}  {value} {units}")
else:
    print(f"Failed to retrieve data: {response.status_code}")