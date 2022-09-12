import time
from driver import Driver
from proxy import Proxy
from e_mail import Email
from kijiji import Kijiji

if __name__ == "__main__":
    proxy = Proxy(username="metalcapricorn", password="metalcapricorn", host="connect3.mproxy.top", port="29504")
    chrome_driver = Driver("chromedriver.exe")
    driver = chrome_driver.setup_driver(None, False)

    email = Email(driver, "2e6af0bf44c9016665bdc7b83a8f0977")
    email.register()
    del email

    kijiji_acc = Kijiji(driver)
    print(kijiji_acc.register("ubfqaxahrgmytruasien@inbox.lv"))
    time.sleep(99999)



