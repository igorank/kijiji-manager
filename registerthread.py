import time
from proxy import Proxy
from ipchanger import IPChanger
import gsheet
from e_mail import Email
from kijiji import Kijiji
from threading import *
from wx.lib.pubsub import pub
from kijiji_api import KijijiApi
import wx
import resultevent


class ResultEvent(wx.PyEvent):

    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(resultevent.EVT_RESULT_ID)
        self.data = data


class RegisterThread(Thread):
    def __init__(self, notify_window, config, num, proxy, main_sheet):
        Thread.__init__(self)
        self.proxy = proxy
        self.config = config
        self._notify_window = notify_window
        self.want_abort = 0
        self.k_api = KijijiApi(proxy=self.proxy)
        self.num = int(num)
        self.main_sheet = main_sheet

    def run(self):
        """Run Thread."""
        i = 0
        while i < self.num:
            if self.want_abort:
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
            wx.CallAfter(pub.sendMessage, "update", msg="")
            email = Email(self.config['WEBDRIVER']['PATH'], self.config['2CAPTCHA']['API_KEY'],
                          self.config['MAIL_FORWARDING']['EMAIL'], self.config['MAIL_FORWARDING']['PASSWORD'])
            if self.want_abort:
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
            wx.CallAfter(pub.sendMessage, "update", msg="")
            # email_dict = email.register(self, self.proxy)
            email_dict = email.register(self, Proxy(self.config['PROXY_EMAIL']['USERNAME'], self.config['PROXY_EMAIL']['PASSWORD'],
                                                    self.config['PROXY_EMAIL']['HOST'], self.config['PROXY_EMAIL']['PORT'],
                                                    self.config['PROXY_EMAIL']['URL']))
            if not email_dict:
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
            wx.CallAfter(pub.sendMessage, "update", msg="")
            del email
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")

            kijiji_acc = Kijiji(self.config['WEBDRIVER']['PATH'])
            if self.want_abort:
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
            kijiji_dict = kijiji_acc.register(self, self.proxy, email_dict['email'], email_dict['imap_pass'])
            if not kijiji_dict:
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
            wx.CallAfter(pub.sendMessage, "update", msg="")

            user_id, token = self.get_token(email_dict['email'], kijiji_dict['password'])
            if self.want_abort:
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return

            # Добавляем данные в таблицу
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
            if self.want_abort:
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            self.main_sheet.update_cell(empty_email_row, 8, token)
            if self.want_abort:
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
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
        """Abort thread."""
        # Method for use by main thread to signal an abort
        self.want_abort = 1
