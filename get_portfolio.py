from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os
from configparser import ConfigParser
import pygsheets

# Init and parse config file
config = ConfigParser()
config.read('config.ini') # this won't work in python ver >= 3.0

# Define the URL of the broker portal
portal_url = config.get('portal', 'url')

# Get the json file path for the google sheets service account
auth_path = config.get('auth', 'path')

# Authorize google sheets
gc = pygsheets.authorize(service_account_file=auth_path)

# Initialise a chrome driver
options = Options()

# Provide the chrome driver executable path, to avoid version mismatch issues
chrome_path = config.get('chrome', 'path')

# Provide a directory for the browser to persist data.
# Doing this makes sure you can "remember this device" 
# and don't need to go through 2FA every time
cache_path = config.get('cache', 'path')
options.add_argument("user-data-dir=" + cache_path)

# Disable automation  (see: https://stackoverflow.com/q/43571119/3772543)
options.add_experimental_option("useAutomationExtension",False)

# Apply preferences and create chrome handle
chrome = webdriver.Chrome(chrome_path, options=options)

chrome.set_page_load_timeout(10)

# Open the web page
chrome.get(portal_url)

time.sleep(5)

data = []

items = chrome.find_elements_by_class_name('investment-item')
for index in range(len(items)):
    items[index].click()

    # Ticker
    ticker = chrome.find_element_by_css_selector('.instrument-type-market .ticker').text

    # Name
    name = chrome.find_element_by_css_selector('.invest-instrument-advanced-header .instrument-name .text').text

    # Shares
    shares = chrome.find_element_by_css_selector('.row.shares .column[data-qa-shares="shares"').text.split(None, 1)

    # Average Price
    avg_price = chrome.find_element_by_css_selector('[data-qa-average-price="average-price"] .value').text.split(None, 1)
    
    # Sell Price
    sell_price = chrome.find_element_by_css_selector('[data-qa-sell-price="sell-price"] .value').text

    # Return
    return_value = chrome.find_element_by_css_selector('[data-qa-return-value="return-value"] .value').text
    
    data.append([
        ticker, 
        name, 
        shares[0], 
        avg_price[0],
        sell_price,
        return_value
    ])


df = pd.DataFrame(data, columns=["Ticker", "Name", "Shares", "Average Price", "Sell Price", "Return Value"])

# Save data to Google sheet titled 'Py to Gsheet Test'
sh = gc.open('PY to Gsheet Test')
wks = sh[0]
wks.set_dataframe(df,(1,1))
# print(df)

# Close and exit chrome
time.sleep(15)
chrome.quit()