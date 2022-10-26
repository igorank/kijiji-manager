import random
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import seleniumwire.undetected_chromedriver.v2 as uc
from useragent import UserAgent


class Driver:

    def __init__(self, chrome_p) -> None:
        super().__init__()
        self.chromedriver_path = chrome_p
        self.headless = False
        self.useragents = UserAgent("useragents\\useragents_win.txt")
        self.useragent = None

    def get_useragent(self) -> str:
        return self.useragent

    def setup_driver(self, proxy=None, headless=True, undetected=False, twocaptcha_ext=True):
        if undetected:
            chrome_options = uc.ChromeOptions()
        else:
            chrome_options = Options()
            if twocaptcha_ext:
                chrome_options.add_extension('extensions\\3.0.9_0.crx')
        # chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.useragent = random.choice(self.useragents)
        chrome_options.add_argument(f'--user-agent="{self.useragent}"')
        # chrome_options.add_argument(f'--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
        #                             f'KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"')

        if headless:
            chrome_options.add_argument("--headless=chrome")

        args = ["hide_console", ]

        if proxy is not None:
            options = {
                'proxy': {
                    'http': 'socks5://' + proxy.get_username() + ':' + proxy.get_password() + '@' + proxy.get_host()
                            + ':' + str(proxy.get_port()),
                    'https': 'socks5://' + proxy.get_username() + ':' + proxy.get_password() + '@' + proxy.get_host()
                             + ':' + str(proxy.get_port()),
                    'no_proxy': 'localhost,127.0.0.1'
                }
            }
            if undetected:
                driver = uc.Chrome(options=chrome_options, seleniumwire_options=options, service_args=args,
                                   use_subprocess=True)
            else:
                driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=options, service_args=args)
        else:
            if undetected:
                driver = uc.Chrome(options=chrome_options, service_args=args, use_subprocess=True)
            else:
                driver = webdriver.Chrome(options=chrome_options, service_args=args)

        return driver
