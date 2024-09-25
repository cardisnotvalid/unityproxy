from .abc import BaseProxy
from .utils import parse_line


class Proxy(BaseProxy):
    def __init__(self, host, port, scheme, username=None, password=None):
        super().__init__(host, port, scheme, username, password)
        self._adapter = None

    @property
    def adapter(self):
        if not self._adapter:
            self._adapter = ProxyAdapter(self)
        return self._adapter

    @classmethod
    def from_data(cls, data, default_scheme="http"):
        return cls(
            host=data.get("host"),
            port=data.get("port"),
            scheme=data.get("scheme", default_scheme),
            username=data.get("username"),
            password=data.get("password")
        )

    @classmethod
    def from_line(cls, line, default_scheme="http", custom_parser=None):
        if custom_parser:
            data = custom_parser(line)
        else:
            data = parse_line(line)
        if data:
            return cls.from_data(data, default_scheme)
        raise ValueError(f"Failed to parse line: {line}")


class ProxyAdapter:
    def __init__(self, proxy):
        self._proxy = proxy

    @property
    def requests(self):
        return {
            "http": self._proxy.uri,
            "https": self._proxy.uri
        }

    @property
    def httpx(self):
        return {
            "http://": self._proxy.uri,
            "https://": self._proxy.uri
        }

    @property
    def pyrogram(self):
        return {
            "scheme": self._proxy.scheme,
            "hostname": self._proxy.host,
            "port": self._proxy.port,
            "username": self._proxy.username,
            "password": self._proxy.password
        }

