'''import datetime
current_year = datetime.datetime.now().year
print(current_year)  # Uses current year if config.toml not specified'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from sys import platform
import toml

def get_year_from_config() -> int:
    data = toml.load("./config.toml")

    if "YEAR" in data:
        return data["YEAR"]

    else:
        import datetime
        current_year = datetime.datetime.now().year
        return current_year  # Uses current year if config.toml not specified


options = Options()
options.add_experimental_option("detach", True)  # Keep browser open
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--disable-blink-features=AutomationControlled")

if platform == "linux" or platform == "linux2":
    options.binary_location = "/usr/bin/brave"  # I used Brave on my linux Machine

driver = webdriver.Chrome(options=options)

web = "https://www.senate.gov/legislative/votes_new.htm"

driver.get(web)


print(get_year_from_config())
#driver.close()