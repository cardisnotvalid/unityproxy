import re

from .exceptions import ProxyParseError


_RE_SCHEME = r"(?P<scheme>\w+)://"
_RE_HOST = r"(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
_RE_PORT = r"(?P<port>\d{1,5})"
_RE_USERNAME = r"(?P<username>[a-zA-Z0-9._-]+)"
_RE_PASSWORD = r"(?P<password>[a-zA-Z0-9._-]+)"
_RE_SEPARATORS = r"[:;@,]"


def _build_regex(*regexs):
    return _RE_SEPARATORS.join(regexs)


_RE_ADDRESS = _build_regex(_RE_HOST, _RE_PORT)
_RE_ADDRESS_AUTH = _build_regex(_RE_USERNAME, _RE_PASSWORD, _RE_ADDRESS)
_RE_ADDRESS_AUTH_REV = _build_regex(_RE_ADDRESS, _RE_USERNAME, _RE_PASSWORD)


def parse_line(line):
    for regex in [_RE_ADDRESS_AUTH_REV, _RE_ADDRESS_AUTH, _RE_ADDRESS]:
        if match := re.search(regex, line):
            attrs = match.groupdict()
            if attrs.get("port"):
                attrs["port"] = int(attrs["port"])

            if match := re.search(_RE_SCHEME, line):
                attrs["scheme"] = match.group(1)

            return attrs
    return {}


class BaseProxy:
    def __init__(self, host, port, scheme, username=None, password=None):
        self.host = host
        self.port = port
        self.scheme = scheme
        self.username = username
        self.password = password

    def __str__(self):
        return f"Proxy({self.uri})"

    def __repr__(self):
        return f"Proxy({self.uri})"

    def is_auth(self):
        return self.username is not None and self.password is not None

    @property
    def uri(self):
        auth = f"{self.username}:{self.password}@" if self.is_auth() else ""
        return f"{self.scheme}://{auth}{self.host}:{self.port}"


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
        raise ProxyParseError(line)


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

