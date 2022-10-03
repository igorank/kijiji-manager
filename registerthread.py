import time
from ipchanger import IPChanger
import gsheet
from proxy import Proxy
from e_mail import Email
from kijiji import Kijiji
from gsheet import GSheet
from threading import *
from wx.lib.pubsub import pub
from kijiji_api import KijijiApi
import wx
import resultevent

# proxy = Proxy(username="SUV4FU", password="eT3PAwKEqavC", host="oproxy.site", port="12536",
#               url="https://mobileproxy.space/reload.html?proxy_key=d7b59504de76caa1d494e882584cca74")
#
# # chrome_driver = Driver("chromedriver.exe")
# # driver = chrome_driver.setup_driver(proxy=proxy, undetected=True, twocaptcha_ext=False, headless=False)
#
# email = Email("chromedriver.exe", "2e6af0bf44c9016665bdc7b83a8f0977")
# email_dict = email.register(proxy)
# del email
# print(email_dict)
#
# kijiji_acc = Kijiji("chromedriver.exe")
# print(kijiji_acc.register(proxy, email_dict['email'], email_dict['imap_pass']))
# # print(kijiji_acc.register(email_dict['email'], email_dict['imap_pass']))


class ResultEvent(wx.PyEvent):

    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(resultevent.EVT_RESULT_ID)
        self.data = data


class RegisterThread(Thread):
    def __init__(self, notify_window, num):
        Thread.__init__(self)
        self.proxy = Proxy(username="SUV4FU", password="eT3PAwKEqavC", host="oproxy.site", port="12536",
                      url="https://mobileproxy.space/reload.html?proxy_key=d7b59504de76caa1d494e882584cca74")
        self._notify_window = notify_window
        self._want_abort = 0
        self.k_api = KijijiApi(proxy=self.proxy)
        self.num = int(num)
        gsheets = GSheet("1gO3m2DJmO6Lwf27Wjustop9eyik9TGO5_9MeJZbetP0", "kijiji-362509-c751d3f68ea1.json")
        self.main_sheet = gsheets.get_main_worksheet(0)
        self.start()

    def run(self):
        """Run Worker Thread."""
        i = 0
        while i < self.num:
            wx.CallAfter(pub.sendMessage, "update", msg="")
            email = Email("chromedriver.exe", "2e6af0bf44c9016665bdc7b83a8f0977")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            email_dict = email.register(self.proxy)
            wx.CallAfter(pub.sendMessage, "update", msg="")
            del email
            wx.CallAfter(pub.sendMessage, "update", msg="")
            print(email_dict)
            wx.CallAfter(pub.sendMessage, "update", msg="")

            kijiji_acc = Kijiji("chromedriver.exe")
            kijiji_dict = kijiji_acc.register(self.proxy, email_dict['email'], email_dict['imap_pass'])
            # print(kijiji_dict['cookies'])
            #kijiji_dict = kijiji_acc.register(proxy, "dadadafoiafnoiafo@inbox.lv", "53653521")
            wx.CallAfter(pub.sendMessage, "update", msg="")

            user_id, token = self.get_token(email_dict['email'], kijiji_dict['password'])

            ## Добавляем данные в таблицу
            empty_email_row = gsheet.get_empty_row_in_col(self.main_sheet, 2)
            self.main_sheet.update_cell(empty_email_row, 1, user_id)
            # Добавляем адр. почти в табл. (1 - стоблец с почт.)
            self.main_sheet.update_cell(empty_email_row, 2, email_dict['email'])
            # Добавляем пароль от kijiji в табл. (2 - стоблец с пар. от почты)
            self.main_sheet.update_cell(empty_email_row, 3, kijiji_dict['password'])
            # Добавляем пароль от почти в табл. (3 - стоблец с пар. от почты)
            self.main_sheet.update_cell(empty_email_row, 4, email_dict['email_pass'])
            # Добавляем IMAP пароль от почти в табл. (4 - стоблец с пар. от почты)
            self.main_sheet.update_cell(empty_email_row, 5, email_dict['imap_pass'])
            # Добавляем Forwarding to в табл. (5 - стоблец с пар. от почты)
            self.main_sheet.update_cell(empty_email_row, 6, email_dict['forwarding_email'])
            # Добавляем UserAgent в табл. (6 - стоблец с пар. от почты)
            self.main_sheet.update_cell(empty_email_row, 7, email_dict['useragent'])
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            self.main_sheet.update_cell(empty_email_row, 8, token)
            wx.CallAfter(pub.sendMessage, "update", msg="")

            i += 1
            wx.CallAfter(pub.sendMessage, "update", msg="")
        wx.PostEvent(self._notify_window, ResultEvent("Done"))

    def get_token(self, email, password):
        it = 0
        while True:
            if it > 2:
                IPChanger.change_ip(self.proxy.get_change_ip_url())  # меняем IP
                it = 0
            try:
                user_id, token = self.k_api.login(email, password)
                break
            except:
                time.sleep(5)
                it += 1
        return user_id, token

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1
