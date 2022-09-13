import time
from driver import Driver
from proxy import Proxy
from e_mail import Email
from kijiji import Kijiji

if __name__ == "__main__":
    proxy = Proxy(username="SUV4FU", password="eT3PAwKEqavC", host="oproxy.site", port="12536",
                  url="https://mobileproxy.space/reload.html?proxy_key=d7b59504de76caa1d494e882584cca74")

    # chrome_driver = Driver("chromedriver.exe")
    # driver = chrome_driver.setup_driver(proxy=proxy, undetected=True, twocaptcha_ext=False, headless=False)

    email = Email("chromedriver.exe", "2e6af0bf44c9016665bdc7b83a8f0977")
    email_dict = email.register(proxy)
    del email
    print(email_dict)

    kijiji_acc = Kijiji("chromedriver.exe")
    print(kijiji_acc.register(proxy, email_dict['email'], email_dict['imap_pass']))
    # print(kijiji_acc.register(email_dict['email'], email_dict['imap_pass']))
    time.sleep(99999)



