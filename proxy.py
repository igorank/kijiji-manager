# from singletonmeta import SingletonMeta


class ProxyException(Exception):
    """Proxy class exception"""


# class Proxy(metaclass=SingletonMeta):
class Proxy:

    def __init__(self, username, password, host, port, url):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.change_ip_url = url

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_change_ip_url(self):
        return self.change_ip_url
