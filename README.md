# Export Trading 212 Portfolio
This script lets you export your Trading 212 portfolio to a Google sheet.

# General Workflow
1. The script opens a "nearly" headless chrome (the GUI is shown at execution time).
2. Login to Trading 212 and save this device (where 2FA is switched on).
3. Read and extract data using css selectors and place into a dataframe.
4. Save the dataframe into a Google sheet and close chrome.

# Setup
1. Clone this repository onto your computer.
2. Download and install the relevant Chrome WebDriver from [here](http://chromedriver.chromium.org/downloads).
3. Create a Google sheet and setup a [service account for pygsheets](https://pygsheets.readthedocs.io/en/stable/authorization.html).
4. Copy sample.config.ini to config.ini and set your options.
5. run `python get_portfolio.py`