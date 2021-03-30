from Agent import Agent, Agenda
from selenium import webdriver
import logging
from time import sleep
from config import config
from selenium.webdriver.chrome.options import Options
import psycopg2
import os
from Crypto.PublicKey import RSA

logging.basicConfig(level=logging.INFO)
key = RSA.importKey(os.environ['PRIV'])

day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def decrypt(cypher):
    return key.decrypt(bytes.fromhex(cypher)).decode('utf-8')

def int_to_str(time):
    out = str(time)
    if (len(out) == 2):
        out = out + ":00"
    elif (len(out) == 1):
        out = out + "0:00"
    else:
        out = "00:00"
    return out


def json_to_agend(json):
    
    for day in day_names:


class Row():
    def __init__(self, result):
        self.agenda_json, self.date, _, _, self.nb_worker, self.stop, self.pas42, self.user42, self.mail = result
        self.pas42 = decrypt(self.pas42)
        self.user42 = decrypt(self.user42)


conn = psycopg2.connect(
    host="ec2-3-233-43-103.compute-1.amazonaws.com",
    database="d1ulnnkdooqel6",
    user="hujazqtsmfiylz",
    password="77a3f43b3a4ec771296738ebc816ec9757e36344aef065a3842e33c804227f31"
)


cur = conn.cursor()
print('PostgreSQL database version:')
cur.execute('SELECT * FROM results')
# print(cur.fetchone())
row = Row(cur.fetchone())
print(getattr(row, 'agenda_json'))

# chrome_options = Options()
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument('window-size=1920x1080')
# # chrome_options.add_argument('window-size=1280x1024')

# def loop(users):


# driver = webdriver.Chrome("./drivers/chromedriver_linux", options= chrome_options)
# wanted = Agenda(wednesday_start='10:00', wednesday_end='17:00', thursday_start='10:00', thursday_end="17:00", friday_start='10:00', friday_end='17:00')
# majordomo = Agent(wanted, driver, 10)
# majordomo.login("jbarment", "69@TheEelHouse!")
# sleep(2)
# majordomo.make_week()
# # majordomo.work()
# driver.close()