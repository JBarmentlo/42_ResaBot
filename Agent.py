from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, NoSuchWindowException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import logging
from time import sleep
from config import config

class Popup():
    def __init__(self, element):
        self.element = element
        # self.occupied = self.get_occupied()
        # self.available = self.get_available()
        self.buttone = self.get_subscribe_button()
        

    def get_occupied(self):
        try:
            return int(self.element.find_element_by_xpath(".//div[@class='modal-card-head-banner']/span[2]/span[2]").text.split("/")[0])
        except Exception as e:
            logging.error(f"Could not get occupied seats frommodal card.\n {e}")
            return 100


    def get_available(self):
        try:
            return int(self.element.find_element_by_xpath(".//div[@class='modal-card-head-banner']/span[2]/span[2]").text.split("/")[1])
        except Exception as e:
            logging.error(f"Could not get available seats frommodal card.\n {e}")
            return 100

    
    def get_subscribe_button(self):
        try:
            buttone = self.element.find_element_by_xpath(".//footer/div/button")
            if ("subscribe" not in buttone.get_property("innerText")):
                logging.error(f"subscribe not in button innertext. innerText: {buttone.get_property('innerText')}")
            return buttone
        except Exception as e:
            logging.error(f"error on get subscribe button \n{e}")
            return None

    def is_subscribed(self):
        print(self.buttone.get_property("innerText"))
        return (self.buttone.get_property("innerText") == "unsubscribe")


    def is_button_disabled(self):
        return (self.buttone.get_property("disabled"))

    def subscribe(self):
        if (self.is_button_disabled()):
            logging.info("Subscibe button disabled")
            return (False)
        try:
            if (self.is_subscribed()):
                logging.error("Attempting to subscribe to already subscribed button")
                return False
            self.buttone.click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@role='alertdialog']")))
            try:
                driver.find_element_by_xpath("//div[@class='notices is-bottom']//button").click()
            except:
                logging.warn("couldnt click away the confirmation banner")
            return True
        except TimeoutException as e:
            logging.error(f"No confirmation banner after click \n{e}")
            return False

    def usnsubscribe(self):
        if (self.is_button_disabled()):
            logging.info("Unsubscibe button disabled")
            return (False)
        try:
            if (not self.is_subscribed()):
                logging.error("Attempting to unsubscribe fromnot subscribed button")
                return False
            self.buttone.click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@role='alertdialog']")))
            try:
                driver.find_element_by_xpath("//div[@class='notices is-bottom']//button").click()
            except:
                logging.warn("couldnt click away the confirmation banner")
            return True
        except Exception as e:
            logging.error(f"No confirmation banner after click \n{e}")
            return False


def catch_popup(driver):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='modal-card-head-banner']//i[@class='mdi mdi-timer default']")))
        return Popup(driver.find_element_by_xpath("//div[@class='modal-card']"))
    except Exception as e:
        logging.error(f"Tried to catch unexisting popup. \n {e}")


def is_stale(element):
    # try:
    #     WebDriverWait(driver, 0).until_not(EC.staleness_of(element))
    #     return False
    # except TimeoutException:
    #     return True
    try:
        element.is_enabled()
        return False
    except StaleElementReferenceException:
        return True

def press_ESC(driver):
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

class Agenda():
    def __init__(self, monday_start = None, monday_end = None, tuesday_start = None, tuesday_end = None, wednesday_start = None, wednesday_end = None, thursday_start = None,
                 thursday_end = None, friday_start = None, friday_end = None, saturday_start = None, saturday_end = None, sunday_start = None, sunday_end = None):
        self.monday_start = monday_start
        self.monday_end = monday_end
        self.tuesday_start = tuesday_start
        self.tuesday_end = tuesday_end
        self.wednesday_start = wednesday_start
        self.wednesday_end = wednesday_end
        self.thursday_start = thursday_start
        self.thursday_end = thursday_end
        self.friday_start = friday_start
        self.friday_end = friday_end
        self.saturday_start = saturday_start
        self.saturday_end = saturday_end
        self.sunday_start = sunday_start
        self.sunday_end = sunday_end
        self.array = [[monday_start, monday_end], [tuesday_start, tuesday_end], [wednesday_start, wednesday_end], [thursday_start, thursday_end], [friday_start, friday_end], [saturday_start, saturday_end], [sunday_start, sunday_end]]


    def is_wanted(self, hour, day_nb):
        return ((hour >= self.array[day_nb][0]) and (hour <= self.array[day_nb][1]))

    def get_wanted_times_day(self, day_nb):
        if (self.array[day_nb][0] is None) or (self.array[day_nb][1] is None):
            return []
        return [x for x in filter(lambda x: self.is_wanted(x, day_nb), config.slot_times)]



class Button():
    def __init__(self, slot, element):
        self.slot = slot
        self.element = element
        self.floor = self.get_floor()
        self.hour = self.get_hour()
        self.reserved = self.get_reserved()


    def get_floor(self):
        try:
            self.floor = self.element.find_element_by_class_name("fc-title").text
        except:
            self.floor = None
            print("SELF FLOOR NONE")
        
        return self.floor


    def get_reserved(self):
        try:
            self.reserved = self.element.find_element_by_xpath(".//i[@class='mdi mdi-calendar-check fc-event-is-subscribe-icon ']") is not None
        except:
            self.reserved = False
        
        return self.reserved


    def get_hour(self):
        try:
            self.hour = self.element.find_element_by_xpath(".//div[@class='fc-time']").get_attribute("data-start")
        except:
            self.hour = None
            print("SELF HOUR = NONE")
    
        return (self.hour)
        

    def refresh(self):
        logging.info("refreshing but")
        try:
            self.element = self.slot.day_element.find_element_by_xpath(f".//a/div/div[@data-start='{self.hour}']/../div[text()='{self.floor}']/../..")
        except StaleElementReferenceException:
            self.slot.refresh()
            self.refresh()


    def click(self):
        try:
            self.element.click()
        except StaleElementReferenceException:
            self.refresh()
            self.click()


    def __str__(self):
        return (f"{self.hour} {self.floor}, reserved: {self.reserved}")



class Slot():
    def __init__(self, day, day_element, hour: str, date = None):
        self.day = day
        self.hour = hour
        self.day_element = day_element
        self.buttons = {}
        self.reserved = False
        self.reserved_floor = None
        self.date = date
        self.set_buttons()
        self.set_reserved()


    def __str__(self):
        return (f"{self.hour}, reserved: {self.reserved_floor}, buttons: {[str(x) for x in self.buttons.values()]}")


    def refresh(self):
        if is_stale(self.day_element):
            self.day_element = self.day.refresh()
        return self.day_element


    def get_buttons(self):
        try:
            return [Button(self, x) for x in self.day_element.find_elements_by_xpath(f".//a/div/div[@data-start='{self.hour}']/../..")]
        except Exception as e:
            print(f"no elements found at {self.hour}")
            print(e)
            return []
        

    def set_buttons(self):
        for but in self.get_buttons():
            self.buttons[but.floor] = but


# REFRESH RESERVED VALEUS ??
    def set_reserved(self):
        reserved = False
        for but in self.buttons.values():
            if (but.reserved):
                self.reserved = True
                self.reserved_floor = but.floor

    
class Day():
    def __init__(self, week, day_element, wanted_times, day_nb):
        self.week = week
        self.day_element = day_element
        self.slots = {}
        self.day_nb = day_nb
        self.get_slots(day_element, wanted_times)

    
    def refresh(self):
        if (is_stale(self.day_element)):
            self.day_element = self.week.refresh()[self.day_nb]
        return (self.day_element)


    def get_slots(self, day_element, wanted_times):
        for hour in wanted_times:
            self.slots[hour] = Slot(self, day_element, hour)

    
    def __str__(self):
        out = config.day_names[self.day_nb] + ":\n"
        for x in self.slots.values():
            out = out + str(x)
            out = out + "\n"
        return (out)

class Week():
    def __init__(self, agenda):
        self.days = []
        self.agenda = agenda
        self.week_element = self.get_week_days()
        self.get_days(agenda, self.week_element)
        logging.info(f"Week object instanciated: \n{self}")


    def refresh(self):
        if (is_stale(self.week_element)):
            self.week_element = self.get_week_days()
        return (self.week_element)


    def get_days(self, agenda, week_element):
        for i in range(7):
            day = Day(self, week_element[i], agenda.get_wanted_times_day(i), i)
            self.days.append(day)


    def get_week_days(self):
        return driver.find_elements_by_xpath("//div[@class='fc-content-skeleton']//div[@class='fc-event-container']")


    def __str__(self):
        out = ""
        for day in self.days:
            out = out + str(day)
            out = out + "\n"
        return (out)

class Agent():
    def __init__(self, agenda, driver):
        self.driver = driver
        self.agenda = agenda
        self.week = None
        self.satisfied = False


    def make_week(self):
        self.week = Week(self.agenda)


    def login(self, login, psswd):
        self.driver.get("https://reservation.42network.org/signin")
        login_field = self.driver.find_element_by_id("user_login")
        psswd_field = self.driver.find_element_by_id("user_password")
        login_field.clear()
        login_field.send_keys(login)
        psswd_field.clear()
        psswd_field.send_keys(psswd)
        psswd_field.send_keys(Keys.RETURN)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//td[@class='fc-widget-content']")))
        logging.info("Logged in.")

    
    def logout(self):
        self.driver.find_elemt_by_xpath("//*[@id='navbar-main']/div[2]/a[2]").click()
        self.driver.find_element_by_xpath("//span[text()='logout']").click()
    

    def spam_slots(self):
        try:
            for day in self.week.days:
                for slot in day.slots.values():
                    logging.debug(str(slot))
                    if (not slot.reserved):
                        for button in slot.buttons.values():
                            logging.debug(str(button))
                            button.click()
                            popup = catch_popup(self.driver)
                            if (popup != None):
                                slot.reserved = popup.subscribe()
                                slot.reserved_floor = button.floor
                            if (slot.reserved):
                                break
                            else:
                                self.satisfied = False
                                ## Doesnt handle slots too close in time
                                press_ESC(self.driver)

        except Exception as e:
            press_ESC(self.driver)
			self.make_week()
            logging.error(f"error whilst reserving iteration \n{e}")
        
    def work(self):
        while (not self.satisfied):
            self.satisfied = True
            self.spam_slots()

logging.basicConfig(level=logging.INFO)
driver = webdriver.Chrome("./chromedriver_linux")
wanted = Agenda(sunday_start='17:00', sunday_end='17:00')
majordomo = Agent(wanted, driver)
majordomo.login("jbarment", "69@TheEelHouse!")
majordomo.make_week()
# majordomo.work()




