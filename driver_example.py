from time import sleep
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# use already logged in user
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=" + os.environ["CHROME_USER_DATA_DIR"])
driver = webdriver.Chrome(executable_path=os.environ["CHROMEDRIVER_LOCATION"], chrome_options=options)

# app logic
driver.get("https://www.twitch.tv/videos/275764362")
#assert "Python" in driver.title
#elem = driver.find_element_by_name("q")
#elem.clear()
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
sleep(10)
driver.get("https://www.twitch.tv/videos/275764844")
sleep(10)
driver.close()

275764362
