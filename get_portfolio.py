from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os
from configparser import ConfigParser

# Init and parse config file
config = ConfigParser()
config.read('config.ini') # this won't work in python ver >= 3.0

# define the URL of the broker portal
portal_url = config.get('portal', 'url')

# Initialise a chrome driver
options = Options()

# Provide a directory for the browser to persist data.
# Doing this makes sure you can "remember this device" 
# and don't need to go through 2FA every time
options.add_argument("user-data-dir=/tmp/paras")

# Disable automation  (see: https://stackoverflow.com/q/43571119/3772543)
options.add_experimental_option("useAutomationExtension",False)

# Apply preferences and create chrome handle
chrome = webdriver.Chrome(options=options)

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

print(df)

# Close and exit chrome
# time.sleep(15)
# chrome.quit()