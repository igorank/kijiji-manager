import requests


class IPChanger:

    @staticmethod
    def change_ip(url):
        if len(url) != 0:
            try:
                requests.get(url, timeout=12)
            except requests.exceptions.ReadTimeout:
                pass
        else:
            return
