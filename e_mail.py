import random
import time
import os
from ipchanger import IPChanger
from twocaptcha import TwoCaptcha
from tempmail import GuerrillaMail
from filemanager import FileManager
from randomuserpass import RandomGenerator
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class Email:

    def __init__(self, driver, twocaptcha_token):
        super().__init__()
        self.driver = driver
        self.names = FileManager.get_filesdata('names\\names_eng.txt')
        self.surnames = FileManager.get_filesdata('names\\surnames_eng.txt')
        self.twocaptcha_token = twocaptcha_token

    def register(self):
        solver = TwoCaptcha(self.twocaptcha_token)
        self.driver.get("https://www.microsoft.com/en-us/microsoft-365/outlook/email-and-calendar-software-microsoft"
                        "-outlook")
        WebDriverWait(self.driver, 25).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="dynamicmarketredirect-dialog-close"]')))
        self.driver.find_element(By.XPATH, '//*[@id="dynamicmarketredirect-dialog-close"]').click()
        self.driver.find_element(By.XPATH, '//*[@id="office-Hero5050-e0h0pts"]/section/div[1]/div[1]/div/div/div/div/div[1]/a').click()

        # Поле ввода email
        self.driver.switch_to.window(self.driver.window_handles[-1])
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="MemberName"]')))
        self.driver.find_element(By.XPATH, '//*[@id="MemberName"]').send_keys(
            RandomGenerator.random_username(14))

        # Нажать Далее
        self.driver.find_element(By.XPATH, '//*[@id="iSignupAction"]').click()

        # Вводим пароль
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="PasswordInput"]')))
        self.driver.find_element(By.XPATH, '//*[@id="PasswordInput"]').send_keys(
            RandomGenerator.random_password(12) + "_" + str(random.randint(10, 99)))

        # Нажать Далее
        self.driver.find_element(By.XPATH, '//*[@id="iSignupAction"]').click()

        # Вводим имя и фамилию
        name = random.choice(self.names)
        surname = random.choice(self.surnames)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="LastName"]')))
        self.driver.find_element(By.XPATH, '//*[@id="LastName"]').send_keys(
            surname)
        self.driver.find_element(By.XPATH, '//*[@id="FirstName"]').send_keys(
            name)

        # Нажать Далее
        self.driver.find_element(By.XPATH, '//*[@id="iSignupAction"]').click()

        # Выбираем дату рождения
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//select[@class="datepart0 form-control win-dropdown"]')))
        d_select = Select(self.driver.find_element(By.XPATH, '//select[@class="datepart0 form-control win-dropdown"]'))
        d_select.select_by_value(str(random.randint(1, 28)))
        m_select = Select(self.driver.find_element(By.XPATH, '//select[@class="datepart1 form-control win-dropdown"]'))
        m_select.select_by_value(str(random.randint(1, 12)))
        self.driver.find_element(By.XPATH, '//*[@id="BirthYear"]').send_keys(
            str(random.randint(1980, 2002)))

        # Нажать Далее
        self.driver.find_element(By.XPATH, '//*[@id="iSignupAction"]').click()

        # Решаем капчу
        # WebDriverWait(self.driver, 60).until(
        #     EC.visibility_of_element_located((By.CLASS_NAME, 'sc-bdnxRM gonizE sc-kEqXSa gjCYOu')))
        # self.driver.find_element(By.CLASS_NAME, 'sc-bdnxRM gonizE sc-kEqXSa gjCYOu').click()
        WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located((By.XPATH,
                                        '//*[@id="HipEnforcementForm"]/div[1]')))
        print("bingo")
        # token = self.driver.execute_script('document.querySelector("#enforcementFrame")')
        #print(token)

        element1 = self.driver.find_element(By.XPATH,'//*[@id="enforcementFrame"]').get_attribute("outerHTML")
        print(element1)

        result = solver.funcaptcha(sitekey='B7D8911C-5CC8-A9A3-35B0-554ACEE604DA',
                                   url='https://signup.live.com/',
                                   surl='https://client-api.arkoselabs.com')

        print('result: ' + str(result))

        # WebDriverWait(self.driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH,
        #                                       '//input[@id="FunCaptcha-Token"]')))
        # print("bingo2")
        # token = self.driver.find_element(By.XPATH,
        #                                 '//input[@id="FunCaptcha-Token"]').get_attribute('value')
        # print(token)


        time.sleep(99999)
