import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    TimeoutException
from twocaptcha import TwoCaptcha
from twocaptcha.api import ApiException
from driver import Driver
from ipchanger import IPChanger
from tempmail import GuerrillaMail
from filemanager import FileManager
from imapreader import EmailReader
from randomuserpass import RandomGenerator


class Email(Driver):

    def __init__(self, chrome_path, twocaptcha_token, forw_email, forw_email_pass):
        super().__init__(chrome_p=chrome_path)
        self.names = FileManager.get_filesdata('names\\names_eng.txt')
        self.surnames = FileManager.get_filesdata('names\\surnames_eng.txt')
        self.twocaptcha_api_key = twocaptcha_token
        self.successful_registrations = 0

        self.forw_email = forw_email
        self.forw_email_pass = forw_email_pass

    @staticmethod
    def press_ok(driver):
        WebDriverWait(driver, 10).until(EC.alert_is_present())  # ERROR
        driver.switch_to.alert.accept()

    def settings_captcha_solver(self, driver):
        if len(driver.window_handles) >= 2:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.switch_to.window(driver.window_handles[-1])
        driver.get("chrome-extension://ifibfemgeogfhoebkmokieepdoobkbpo/options/options.html")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input")))
        driver.find_element("xpath", "/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input"). \
            send_keys(self.twocaptcha_api_key)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/form/div[2]/table/tbody/tr[5]/td[2]/div[2]/input")))
        driver.find_element("xpath",
                            "/html/body/div/form/div[2]/table/tbody/tr[5]/td[2]/div[2]/input").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/div/div[1]/table/tbody/tr[1]/td[3]/button")))
        driver.find_element("xpath", "/html/body/div/div[1]/table/tbody/tr[1]/td[3]/button").click()
        self.press_ok(driver)

    @staticmethod
    def get_last_emailid(guerrilla_mail, thread):
        last_email_id = guerrilla_mail.get_last_email_id()
        while True:
            if last_email_id != 1:
                break
            if thread.want_abort:
                return False
            time.sleep(1)
            last_email_id = guerrilla_mail.get_last_email_id()
        return last_email_id

    @staticmethod
    def terms_agree(driver, thread):
        it = 0
        while it <= 10:
            try:
                driver.find_element("xpath", "/html/body/div[5]/div/div/div[3]/button[2]").click()
                return True
            except NoSuchElementException:
                time.sleep(1)
                it += 1
                continue
        if thread.want_abort:
            return 2
        return False

    @staticmethod
    def get_imap_pass(driver, delay, thread):
        it = 0
        while it <= delay:
            imap_pass = driver.find_element(By.ID,
                                            "pop3-pass-field").get_attribute('value')
            if len(imap_pass) == 0:
                time.sleep(1)
                continue
            else:
                return imap_pass
        if thread.want_abort:
            return 1
        return False

    @staticmethod
    def add_email_forwarding(driver, thread, forw_email, password):
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="options-menu_li_forward_list-aliases-forward"]')))
        driver.find_element("xpath",
                            '//*[@id="options-menu_li_forward_list-aliases-forward"]').click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[2]/div[2]/section/article/div/div[1]/div/div[2]/div/a')))
        driver.find_element("xpath",
                            '/html/body/div[2]/div[2]/section/article/div/div[1]/div/div[2]/div/a').click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="eml-forwarding-container"]/div[2]/div[1]/div/input')))
        driver.find_element("xpath",
                            '//*[@id="eml-forwarding-container"]/div[2]/div[1]/div/input').send_keys(
            "ktrhteblpavynbpqniuo@outlook.com")
        driver.find_element("xpath",
                            '//*[@id="btn_add-email"]').click()
        mail_reader = EmailReader("outlook.office365.com", str(forw_email), str(password))
        code = mail_reader.get_forw_code(120, thread)
        if code == -1:
            return False
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="container_prop-content_ol_existing-forwards"]/li/div/form/div/input')))
        driver.find_element("xpath",
                            '//*[@id="container_prop-content_ol_existing-forwards"]/li/div/form/div/input').send_keys(
            str(code))
        driver.find_element("xpath",
                            '//*[@id="container_prop-content_ol_existing-forwards"]/li/div/form/button').click()
        return forw_email

    def register(self, thread, proxy):

        solver = TwoCaptcha(self.twocaptcha_api_key)

        names = FileManager.get_filesdata('names\\names.txt')
        surnames = FileManager.get_filesdata('names\\surnames.txt')

        while self.successful_registrations < 1:
            guerrilla_mail = GuerrillaMail()
            name = random.choice(names)
            surname = random.choice(surnames)
            initialized = False
            if thread.want_abort:
                return False
            driver = self.setup_driver(proxy=proxy, twocaptcha_ext=True, headless=self.headless)
            if thread.want_abort:
                return False
            try:
                self.settings_captcha_solver(driver)
                if thread.want_abort:
                    return False
                initialized = True
                if thread.want_abort:
                    return False
                driver.get("https://login.inbox.lv/")
                if thread.want_abort:
                    return False
                driver.find_element("xpath",
                                    "/html/body/div[1]/article/form/fieldset/div[4]/a").click()
                username = RandomGenerator.random_username(20)
                driver.find_element("xpath",
                                    "/html/body/div[1]/article/div/div/div[2]/form/fieldset/div[1]/div[1]/div["
                                    "1]/div/input").send_keys(
                    username)
                driver.find_element("xpath",
                                    "/html/body/div[1]/article/div/div/div[2]/form/fieldset/div[1]/div[1]/div["
                                    "2]/input").send_keys(
                    name)
                driver.find_element("xpath",
                                    "/html/body/div[1]/article/div/div/div[2]/form/fieldset/div[1]/div[1]/div["
                                    "3]/input").send_keys(
                    surname)
                password = RandomGenerator.random_password(12) + str(random.randint(1000, 9999))
                driver.find_element("xpath",
                                    "/html/body/div[1]/article/div/div/div[2]/form/fieldset/div[1]/div[1]/div["
                                    "4]/div/input").send_keys(
                    password)
                driver.find_element("xpath",
                                    "/html/body/div[1]/article/div/div/div[2]/form/fieldset/div[1]/div[1]/div["
                                    "5]/div/input").send_keys(
                    password)
                driver.find_element("xpath",
                                    "/html/body/div[1]/article/div/div/div[2]/form/fieldset/div[3]/div[1]/div["
                                    "1]/label/input").click()
                response = self.terms_agree(driver, thread)
                if not response:
                    driver.close()
                    driver.quit()
                    IPChanger.change_ip(proxy.get_change_ip_url())
                    continue
                if response == 2:
                    return False
                driver.find_element("xpath",
                                    "/html/body/div[1]/article/div/div/div[2]/form/fieldset/div[3]/div[1]/div["
                                    "2]/label/input").click()
                driver.find_element("xpath",
                                    "/html/body/div[1]/article/div/div/div[2]/form/fieldset/div[3]/div[2]/button") \
                    .click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[5]/div/div/div[2]/div[2]/div[1]/img")))
                if thread.want_abort:
                    return False
                second_try = False
                while True:
                    if thread.want_abort:
                        return False
                    time.sleep(2)  # TEMP solution (for image loading)
                    if second_try:
                        img = driver.find_element(By.XPATH, '//img[@class="captcha__img img-responsive"]')
                    else:
                        img = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[2]/div[2]/div[1]/img')
                    try:
                        result = solver.normal(img.screenshot_as_base64)
                    except ApiException:
                        if thread.want_abort:
                            return False
                        driver.close()
                        driver.quit()
                        IPChanger.change_ip(proxy.get_change_ip_url())
                        continue


                    if second_try:
                        driver.find_element("xpath",
                                            '//*[@id="signup_userpin"]').send_keys(result['code'])
                        driver.find_element(By.XPATH, '//button[@class="btn btn-primary"]').click()  # Подтвердить
                    else:
                        driver.find_element("xpath",
                                            "/html/body/div[5]/div/div/div[2]/div[2]/div[2]/input[2]").send_keys(
                            result['code'])
                        driver.find_element("xpath", "/html/body/div[5]/div/div/div[3]/button[1]").click()

                    try:
                        WebDriverWait(driver, 6).until(
                            EC.invisibility_of_element_located(
                                (By.XPATH, "/html/body/div[5]/div/div/div[2]/div[2]/div[1]/img")))
                        if thread.want_abort:
                            return False
                    except TimeoutException:
                        if thread.want_abort:
                            return False
                        solver.report(result['captchaId'], False)
                        continue

                    if thread.want_abort:
                        return False
                    h_captcha_result = check_hcaptcha(driver, thread)
                    if h_captcha_result == 1:
                        if thread.want_abort:
                            return False
                        driver.find_element("xpath",
                                            "/html/body/div[1]/div[2]/div/div/div[2]/form/fieldset/div/button").click()
                        driver.get(
                            "https://email.inbox.lv/?utm_source=portal&utm_medium=vertical&utm_term=ru&utm_campaign"
                            "=toolbar")
                        if thread.want_abort:
                            return False
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "/html/body/div/div/div/div/div[5]/div/a")))
                        driver.find_element("xpath",
                                            "/html/body/div/div/div/div/div[5]/div/a").click()  # button next
                        driver.find_element("xpath",
                                            "/html/body/div/div/div/div/div[4]/a").click()  # button back
                        if thread.want_abort:
                            return False
                        email = guerrilla_mail.get_email_add()
                        if thread.want_abort:
                            return False
                        driver.find_element("xpath",
                                            "/html/body/div/div/div/div/form/fieldset/div/input").send_keys(
                            str(email))  # second email field
                        driver.find_element("xpath",
                                            "/html/body/div/div/div/div/div[3]/button").click()  # button next
                        if thread.want_abort:
                            return False
                        last_email_id = self.get_last_emailid(guerrilla_mail, thread)
                        if not last_email_id:
                            return False
                        email_body = guerrilla_mail.get_email_body(last_email_id)
                        ver_code = guerrilla_mail.get_inboxlv_code(email_body)
                        if thread.want_abort:
                            return False
                        driver.find_element("xpath",
                                            "/html/body/div/div/div/div/div[3]/div/form/div[1]/div[2]/input").send_keys(
                            str(ver_code))  # code field
                        driver.find_element("xpath",
                                            "/html/body/div/div/div/div/div[3]/div/form/div[1]/div[3]/button").click()
                        driver.find_element("xpath",
                                            "/html/body/div/div/div/div/div[3]/a").click()  # Next button
                        day = '0' + str(random.randint(1, 9))
                        d_select = Select(driver.find_element(By.ID, "bday"))
                        d_select.select_by_value(day)
                        month = '0' + str(random.randint(1, 9))
                        m_select = Select(driver.find_element(By.NAME, "_bmon"))
                        m_select.select_by_value(month)
                        year = str(random.randint(1990, 1999))
                        driver.find_element("xpath",
                                            "/html/body/div/div/div/div/form/div[1]/div/input").send_keys(year)
                        sex_select = Select(
                            driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div[2]/div/select"))
                        sex_select.select_by_value(str(0))
                        driver.find_element("xpath",
                                            "/html/body/div/div/div/div/form/div[4]/button").click()  # Next Button
                        driver.find_element("xpath",
                                            "/html/body/div/div/div/div/div[3]/div/a").click()  # Ready button
                        if thread.want_abort:
                            return False
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[3]/nav/ul/li[7]/a")))  # settings button
                        driver.find_element("xpath",
                                            "/html/body/div[3]/nav/ul/li[7]/a").click()  # settings button
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH,
                             "/html/body/div[2]/div[2]/section/aside/nav/ul/li[7]/a")))  # Outlook, почтовые программы
                        driver.find_element("xpath",
                                            "/html/body/div[2]/div[2]/section/aside/nav/ul/li[7]/a").click()
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH,
                             "/html/body/div[2]/div[2]/section/article/div/div/div/div[2]/div/button")))  # Включить
                        driver.find_element("xpath",
                                            "/html/body/div[2]/div[2]/section/article/div/div/div/div["
                                            "2]/div/button").click()
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.ID, "pop3-pass-field")))  # pop3-pass-field
                        imap_pass = self.get_imap_pass(driver, 15, thread)
                        if not imap_pass:
                            driver.close()
                            driver.quit()
                            IPChanger.change_ip(proxy.get_change_ip_url())
                            continue
                        if imap_pass == 1:
                            return False
                        driver.find_element("xpath", '//*[@id="pop3-pass-modal-submit"]').click()  # OK Button
                        if thread.want_abort:
                            return False
                        if self.forw_email and self.forw_email_pass:
                            if thread.want_abort:
                                return False
                            forw_email = self.add_email_forwarding(driver, thread, self.forw_email,
                                                                   self.forw_email_pass)
                            if not forw_email:
                                return False
                            if thread.want_abort:
                                return False
                        else:
                            forw_email = ""
                        if thread.want_abort:
                            return False
                        self.successful_registrations += 1
                        driver.close()
                        driver.quit()
                        if thread.want_abort:
                            return False
                        data = {'email': username + "@inbox.lv", 'email_pass': str(password),
                                'imap_pass': str(imap_pass), 'useragent': self.get_useragent(),
                                'forwarding_email': forw_email}
                        return data
                    if h_captcha_result == -1:
                        driver.close()
                        driver.quit()
                        IPChanger.change_ip(proxy.get_change_ip_url())
                        break
                    if h_captcha_result == 0:
                        second_try = True
                        driver.find_element(By.XPATH, '//button[@class="btn btn-default"]').click()  # Отмена
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="signup_submit"]')))
                        driver.find_element(By.XPATH, '//*[@id="signup_submit"]').click()
                        continue
                    if h_captcha_result == 2:
                        return False
            except (ElementClickInterceptedException, TimeoutException):
                if thread.want_abort:
                    return False
                if initialized:
                    driver.close()
                    driver.quit()
                    IPChanger.change_ip(proxy.get_change_ip_url())
                continue


def check_hcaptcha(driver, thread) -> int:
    errors = ["Слишком много попыток регистрации. Попробуйте позже.", "API_HTTP_CODE_500",
               "API_HTTP_CODE_521",
              "Ошибка создания новой учётной записи. Попробуйте повторить через 5 минут."]

    it = 0
    while it < 90:

        if thread.want_abort:
            return 2

        try:
            if driver.find_element("xpath",
                                   "/html/body/div[1]/div[2]/div/div/div[2]/div/div"):
                return 1
        except NoSuchElementException:
            res = any(ele in driver.page_source for ele in errors)
            if res:
                return -1
            elif "ERROR_SITEKEY" in driver.page_source:
                return 0

        time.sleep(2)
        it += 1
    return -1
