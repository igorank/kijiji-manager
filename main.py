import time
import wx
from gsheet import GSheet
from mainpanel import MainPanel
from driver import Driver
from proxy import Proxy
from e_mail import Email
from kijiji import Kijiji


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
                          title="Kijiji Manager", size=(800, 600))
        panel = MainPanel(self)


class GenApp(wx.App):

    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)

    def OnInit(self):
        # create frame here
        frame = MainFrame()
        frame.Show()
        return True


if __name__ == "__main__":
    # gsheets = GSheet("1gO3m2DJmO6Lwf27Wjustop9eyik9TGO5_9MeJZbetP0", "kijiji-362509-c751d3f68ea1.json")
    # main_sheet = gsheets.get_main_worksheet(0)
    # list_of_hashes = main_sheet.get_all_records()
    # # print(list_of_hashes[0].keys())
    # print(list_of_hashes)

    app = GenApp()
    app.MainLoop()


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
    # time.sleep(99999)
