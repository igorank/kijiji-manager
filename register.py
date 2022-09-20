import time

import gsheet
from proxy import Proxy
from e_mail import Email
from kijiji import Kijiji
from gsheet import GSheet
from threading import *
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


class WorkerThread(Thread):
    def __init__(self, notify_window, num):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.num = int(num)
        gsheets = GSheet("1gO3m2DJmO6Lwf27Wjustop9eyik9TGO5_9MeJZbetP0", "kijiji-362509-c751d3f68ea1.json")
        self.main_sheet = gsheets.get_main_worksheet(0)
        self.start()

    def run(self):
        """Run Worker Thread."""
        # for i in range(10):
        #     time.sleep(1)
        #     print(i)
        #     if self._want_abort:
        #         wx.PostEvent(self._notify_window, ResultEvent(None))
        #         return
        # wx.PostEvent(self._notify_window, ResultEvent(10))
        i = 0
        while i < self.num:
            proxy = Proxy(username="SUV4FU", password="eT3PAwKEqavC", host="oproxy.site", port="12536",
                          url="https://mobileproxy.space/reload.html?proxy_key=d7b59504de76caa1d494e882584cca74")
            email = Email("chromedriver.exe", "2e6af0bf44c9016665bdc7b83a8f0977")
            email_dict = email.register(proxy)
            del email
            print(email_dict)

            # kijiji_acc = Kijiji("chromedriver.exe")
            # print(kijiji_acc.register(proxy, email_dict['email'], email_dict['imap_pass']))

            ## Добавляем данные в таблицу
            # Добавляем адр. почти в табл. (1 - стоблец с почт.)
            empty_email_row = gsheet.get_empty_row_in_col(self.main_sheet, 1)
            self.main_sheet.update_cell(empty_email_row, 1, email_dict['email'])
            # Добавляем пароль от почти в табл. (3 - стоблец с пар. от почты)
            self.main_sheet.update_cell(empty_email_row, 3, email_dict['email_pass'])
            # Добавляем IMAP пароль от почти в табл. (4 - стоблец с пар. от почты)
            self.main_sheet.update_cell(empty_email_row, 4, email_dict['imap_pass'])

            i += 1
        wx.PostEvent(self._notify_window, ResultEvent("Done"))

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1
