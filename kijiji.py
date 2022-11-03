import random
import string
from driver import Driver
from ipchanger import IPChanger
from filemanager import FileManager
from randomuserpass import RandomGenerator
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from imapreader import EmailReader


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
        self.names = FileManager.get_filesdata('names\\names_eng.txt')
        self.surnames = FileManager.get_filesdata('names\\surnames_eng.txt')

    def register(self, thread, proxy, email, imap_pass):
        while True:
            data = dict()
            data['email'] = email

            driver = self.setup_driver(proxy=proxy, undetected=True, twocaptcha_ext=False, headless=True)
            if thread.want_abort:
                driver.close()
                driver.quit()
                return False

            try:
                driver.get("https://www.kijiji.ca/t-user-registration.html")
            except TimeoutException:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            if thread.want_abort:
                driver.close()
                driver.quit()
                return False

            while True:
                if thread.want_abort:
                    driver.close()
                    driver.quit()
                    return False

                try:
                    # WebDriverWait(driver, 20).until(
                    #     EC.presence_of_element_located((By.XPATH, '//*[@id="profileName"]')))
                    WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="profileName"]')))
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="mainPageContent"]/div/div/div/div/div/div/main/form/button')))
                    break
                except:
                    driver.refresh()

            name = random.choice(self.names)
            driver.find_element(By.XPATH, '//*[@id="profileName"]').send_keys(
                name)

            driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(
                email)
            if thread.want_abort:
                driver.close()
                driver.quit()
                return False

            password = RandomGenerator.random_password(8) + random_upper_letter() + '_' + str(random.randint(10, 99))
            data['password'] = password
            driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(
                password)
            driver.find_element(By.XPATH, '//*[@id="passwordConfirmation"]').send_keys(
                password)

            driver.find_element(By.XPATH, '//*[@id="mainPageContent"]/div/div/div/div/div/div/main/form/button').click()
            if thread.want_abort:
                driver.close()
                driver.quit()
                return False

            try:
                WebDriverWait(driver, 15).until(
                    lambda driver: driver.find_elements(By.XPATH, '//*[@id="LocUpdate"]')
                    or driver.find_elements(By.XPATH, '//*[@id="Homepage"]/div[1]/span/div/button'))
                break
            except:
                try:
                    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                    WebDriverWait(driver, 5).until(
                        lambda driver: driver.find_elements(By.XPATH, '//*[@id="LocUpdate"]')
                                       or driver.find_elements(By.XPATH, '//*[@id="Homepage"]/div[1]/span/div/button'))
                    break
                except:
                    if thread.want_abort:
                        driver.close()
                        driver.quit()
                        return False

                    IPChanger.change_ip(proxy.get_change_ip_url())
                    driver.close()
                    driver.quit()
                    continue

                # if thread.want_abort:
                #     driver.close()
                #     driver.quit()
                #     return False
                #
                # IPChanger.change_ip(proxy.get_change_ip_url())
                # driver.close()
                # driver.quit()
                # continue

        if thread.want_abort:
            driver.close()
            driver.quit()
            return False

        mail_reader = EmailReader("mail.inbox.lv", email, imap_pass)
        verf_link = mail_reader.get_verf_link(120, thread)
        if verf_link == -1:
            driver.close()
            driver.quit()
            return False

        cookies = get_cookies(driver)
        data['cookies'] = cookies
        try:
            driver.get(verf_link)
        except TimeoutException:
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        if thread.want_abort:
            driver.close()
            driver.quit()
            return False

        driver.close()
        driver.quit()

        if thread.want_abort:
            driver.close()
            driver.quit()
            return False

        IPChanger.change_ip(proxy.get_change_ip_url())  # меняем IP

        return data
