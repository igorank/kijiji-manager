import time
from imap_tools import MailBox


class EmailReader:

    def __init__(self, server, email, password):
        super().__init__()
        self.mb = MailBox(server).login(str(email), str(password))

    def get_verf_link(self, delay):
        it = 0
        while it <= delay:
            messages = self.mb.fetch()
            for msg in messages:
                if msg.from_ == "donot-reply@kijiji.ca":
                    text = str(msg.html)
                    index = text.find("https://www.kijiji.ca/m-user-activation.html?token=")
                    start = text[index:]
                    link = start.partition('"')[0]
                    return link
            time.sleep(1)
            it += 1
        return False
