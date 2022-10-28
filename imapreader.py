import time
from imap_tools import MailBox


def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")
    return s


class EmailReader:

    def __init__(self, server, email, password):
        super().__init__()
        self.mb = MailBox(server).login(str(email), str(password))

    def get_verf_link(self, delay, thread):
        it = 0
        while it <= delay:
            if thread._want_abort:
                return -1
            messages = self.mb.fetch()
            for msg in messages:
                if msg.from_ == "donot-reply@kijiji.ca":
                    text = str(msg.html)
                    index = text.find("https://www.kijiji.ca/m-user-activation.html?token=")
                    start = text[index:]
                    link = start.partition('"')[0]
                    flink = unescape(link)
                    return flink
            time.sleep(1)
            it += 1
        return False

    def get_forw_code(self, delay, thread):
        it = 0
        while it <= delay:
            if thread._want_abort:
                return -1
            messages = self.mb.fetch()
            for msg in messages:
                if msg.from_ == "support@inbox.lv":
                    text = str(msg.html)
                    index = text.find(
                        'color:white;outline: none;display:inline-block;line-height:50px;margin-bottom:15px;margin-top:15px;">')
                    start = text[index:]
                    code_str = start.partition('</span>')[0]
                    code = code_str[-6:]
                    self.mb.delete(msg.uid)     # удаляем письмо
                    return code
            time.sleep(1)
            it += 1
        return False

