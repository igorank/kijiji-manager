import requests


class IPChanger:

    @staticmethod
    def change_ip(url):
        if len(url) != 0:
            try:
                requests.get(url, timeout=12)
            except:
                pass
        else:
            return

    @staticmethod
    def get_ip(username, password, host, port):
        ip = requests.get('https://api.ipify.org', proxies=dict(
            http='socks5://' + str(username) + ':' + str(password) + '@' + str(host) + ':' + str(port),
            https='socks5://' + str(username) + ':' + str(password) + '@' + str(host) + ':' + str(port))).text
        return ip
