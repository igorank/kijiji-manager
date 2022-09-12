import random
import string
from filemanager import FileManager
from randomuserpass import RandomGenerator
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from imapreader import EmailReader
from selenium.webdriver.support.ui import Select


def random_upper_letter():
    return ''.join(random.choices(string.ascii_uppercase))


class Kijiji:

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.names = FileManager.get_filesdata('names\\names_eng.txt')
        self.surnames = FileManager.get_filesdata('names\\surnames_eng.txt')

    def register(self, email, imap_pass) -> dict:
        data = dict()
        data['email'] = email

        self.driver.get("https://www.kijiji.ca/t-user-registration.html")

        name = random.choice(self.names)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="profileName"]')))
        self.driver.find_element(By.XPATH, '//*[@id="profileName"]').send_keys(
            name)

        self.driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(
            email)

        password = RandomGenerator.random_password(8) + random_upper_letter() + '_' + str(random.randint(10, 99))
        data['password'] = password
        self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(
            password)
        self.driver.find_element(By.XPATH, '//*[@id="passwordConfirmation"]').send_keys(
            password)

        self.driver.find_element(By.XPATH, '//*[@id="mainPageContent"]/div/div/div/div/div/div/main/form/button').click()

        # WebDriverWait(self.driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="LocUpdate"]')))     # проверка регистрации

        mail_reader = EmailReader("mail.inbox.lv", email, imap_pass)
        verf_link = mail_reader.get_verf_link(120)
        self.driver.get(str(verf_link))

        return data

