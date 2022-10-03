import random
import string
from driver import Driver
from ipchanger import IPChanger
from filemanager import FileManager
from randomuserpass import RandomGenerator
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from imapreader import EmailReader
from selenium.webdriver.support.ui import Select


def random_upper_letter():
    return ''.join(random.choices(string.ascii_uppercase))


def get_cookies(driver):
    cookies = driver.get_cookies()
    cookies_dict = {}
    for cookie in cookies:
        cookies_dict[cookie['name']] = cookie['value']
    return cookies_dict


class Kijiji(Driver):

    def __init__(self, chrome_path):
        super().__init__(chrome_p=chrome_path)
        # self.driver = driver
        self.names = FileManager.get_filesdata('names\\names_eng.txt')
        self.surnames = FileManager.get_filesdata('names\\surnames_eng.txt')

    def register(self, proxy, email, imap_pass) -> dict:
        data = dict()
        data['email'] = email

        print('Setting up the driver.', end=' ')
        driver = self.setup_driver(proxy=proxy, undetected=True, twocaptcha_ext=False, headless=False)
        print('Done.')

        driver.get("https://www.kijiji.ca/t-user-registration.html")
        # WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH,
        #                                     '//*[@id="MainContainer"]/div[1]/div/div[2]/div/header/div[3]/div/div[3]/div/div/div/a[1]')))
        while True:
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="profileName"]')))
                break
            except:
                driver.refresh()
        # driver.find_element(By.XPATH, '//a[@title="Register"]').click()

        name = random.choice(self.names)
        # WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="profileName"]')))
        driver.find_element(By.XPATH, '//*[@id="profileName"]').send_keys(
            name)

        driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(
            email)

        password = RandomGenerator.random_password(8) + random_upper_letter() + '_' + str(random.randint(10, 99))
        data['password'] = password
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(
            password)
        driver.find_element(By.XPATH, '//*[@id="passwordConfirmation"]').send_keys(
            password)

        driver.find_element(By.XPATH, '//*[@id="mainPageContent"]/div/div/div/div/div/div/main/form/button').click()

        # WebDriverWait(self.driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="LocUpdate"]')))     # проверка регистрации

        mail_reader = EmailReader("mail.inbox.lv", email, imap_pass)
        verf_link = mail_reader.get_verf_link(120)
        # print(verf_link)
        cookies = get_cookies(driver)
        data['cookies'] = cookies
        driver.get(verf_link)
        driver.close()
        driver.quit()

        # IPChanger.change_ip(proxy.get_change_ip_url()) # меняем IP

        return data

