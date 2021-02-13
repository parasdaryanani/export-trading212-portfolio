# Export Trading 212 Portfolio
This script lets you export your Trading 212 portfolio to a pandas dataframe.

# General Workflow
1. Open a "nearly" headless chrome (the GUI is shown at execution time)
2. Login to Trading 212 and save this device (where 2FA is switched on)
3. Read and extract data using css selectors and place into a dataframe

# Setup
1. Clone this repository onto your computer
2. Download and install the relevant Chrome WebDriver from [here](http://chromedriver.chromium.org/downloads)