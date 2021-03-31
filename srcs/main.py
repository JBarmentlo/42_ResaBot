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


def json_to_agenda(json):
    agenda = Agenda()
    if (json is None):
        return agenda
    for day in day_names:
        d = json[day]
        if (d[0]):
            setattr(agenda, day.lower() + "_start", int_to_str(d[1]))
            setattr(agenda, day.lower() + "_end", int_to_str(d[2]))
    agenda.make_array()
    logging.info(f"Agenda array: {agenda.array}")
    logging.info(f"json: {json}")
    return agenda


class Row():
    def __init__(self, result):
        self.agenda_json, self.date, _, _, self.nb_worker, self.stop, self.pas42, self.user42, self.mail = result
        self.pas42 = decrypt(self.pas42)
        self.user42 = decrypt(self.user42)
        logging.info(f"{self.user42}")
        self.agenda = json_to_agenda(self.agenda_json)

i = 0

def start_chrome(i = 0):
    if (i > 7):
        logging.error("TOO MANY CHROME CRAHSES")
        raise MemoryError
    try:
        driver = webdriver.Chrome(options= chrome_options)
    except Exception as e:
        logging.error(f"Chromedriver crasher \n{e}")
        start_chrome(i + 1)
    logging.ino("chrome started")
    return (driver)
        
def loop(cur):
    cur.execute('SELECT * FROM results')
    for res in cur.fetchall():
        row = Row(res)
        # logging.info(f"going for {str(res)}")
        if (row.stop != 1 and row.agenda != None and (not row.agenda.is_empty())):
            logging.info("scraping")
            start_chrome()
            majordomo = Agent(row.agenda, driver, 5)
            sleep(10)
            # driver.save_screenshot("screenshot1.png")
            majordomo.login(row.user42, row.pas42)
            sleep(10)
            # driver.save_screenshot("screenshot2.png")
            majordomo.make_week()
            majordomo.work()
            majordomo.logout()
            driver.close()
            sleep(20)

if __name__=="__main__":
    logging.info("STARTING APP")
    print("STARTED BABE")
    key = RSA.importKey(os.environ['PRIV'])
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    conn = psycopg2.connect(
        host="ec2-3-233-43-103.compute-1.amazonaws.com",
        database="d1ulnnkdooqel6",
        user="hujazqtsmfiylz",
        password="77a3f43b3a4ec771296738ebc816ec9757e36344aef065a3842e33c804227f31"
    )

    cur = conn.cursor()
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument('window-size=1024×768')

    while (True):
        loop(cur)
        sleep(1000)
    driver.close()

