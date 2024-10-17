'''import datetime
current_year = datetime.datetime.now().year
print(current_year)  # Uses current year if config.toml not specified'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from sys import platform
import toml
import time
import datetime

import pandas as pd

def get_year_from_config() -> int:
    """Reads the year from the config.toml file if it exists, otherwise uses the current year

    Returns:
        int: The year to use
    """
    try:
        data = toml.load("./config.toml")
    except FileNotFoundError:
        current_year = datetime.datetime.now().year
        return current_year # Uses current year if config.toml not present

    if "YEAR" in data:
        return data["YEAR"]

    else:
        current_year = datetime.datetime.now().year
        return current_year  # Uses current year if config.toml not specified

def create_dataframe(columns: list) -> pd.DataFrame:
    """Creates an empty pandas DataFrame with the given columns.

    Args:
        columns (list): A list of strings containing the column names

    Returns:
        pd.DataFrame: An empty Pandas DataFrame with the given column names
    """
    df = pd.DataFrame(columns=columns)

    return df

# Setting up the webdriver
options = Options()
options.add_experimental_option("detach", True)  # Keep browser open
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--disable-blink-features=AutomationControlled")

# I used Brave on my linux Machine
if platform == "linux" or platform == "linux2":
    options.binary_location = "/usr/bin/brave"

driver = webdriver.Chrome(options=options)

web = "https://www.senate.gov/legislative/votes_new.htm"

driver.get(web)

# Select the year specified in the config.toml (Or current year if not specified)
year_element = driver.find_element(By.NAME, 'menu')
select = Select(year_element)
selected_year = get_year_from_config()

# Select the desired year
# The next() function finds the first option where got_year (e.g., "2024") is in the option's text.
select.select_by_visible_text(next(option.text for option in select.options if str(selected_year) in option.text))

# Select All votes during the selected year
items_element = driver.find_element(By.NAME, 'listOfVotes_length')
select = Select(items_element)
select.select_by_visible_text("All")

# Select and loop through the votes
votes_table = driver.find_element('id', 'listOfVotes')

vote_rows = votes_table.find_elements('tag name', 'tr')

# Create Vote Details, Senators and Attendance DataFrames
# (We will export it to a csv file), we specify column names in a list
detail_columns = ['vote_number', 'vote_date', 'result', 'measure_number', 'measure_title']
vote_details_dataframe = create_dataframe(detail_columns)

senator_columns = ['senator_name', 'party', 'state']
senator_dataframe = create_dataframe(senator_columns)
senator_dataframe['senator_number'] = range(1, len(senator_dataframe) + 1)

attendance_columns = ['vote_number', 'senator_number', 'vote']
attendance_dataframe = create_dataframe(attendance_columns)

for row in vote_rows:
    # Get all the columns in this row (typically <td> for data cells)
    columns = row.find_elements('tag name', 'td')

    # Looping through the columns
    for col in columns:
        # Find the <td> element with class "contenttext sorting_1"
        content_td = row.find_element('class name', 'contenttext.sorting_1')

        # Find the <a> tag (link) inside the <td> element
        link = content_td.find_element('tag name', 'a')

        # Click the link, we are inside the vote details page
        link.click()

        # Get the vote details
        break

print(get_year_from_config())
time.sleep(10)

driver.close()
