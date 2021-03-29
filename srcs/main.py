from Agent import Agent, Agenda
from selenium import webdriver
import logging
from time import sleep
from config import config
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.INFO)
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('window-size=1920x1080')
# chrome_options.add_argument('window-size=1280x1024')

driver = webdriver.Chrome("./drivers/chromedriver_linux", options= chrome_options)
wanted = Agenda(wednesday_start='10:00', wednesday_end='17:00', thursday_start='10:00', thursday_end="17:00", friday_start='10:00', friday_end='17:00')
majordomo = Agent(wanted, driver)
majordomo.login("jbarment", "69@TheEelHouse!")
sleep(2)
majordomo.make_week()
majordomo.work()
driver.close()