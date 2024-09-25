import os
import re
import json


_RE_SCHEME = r"(?P<scheme>\w+)://"
_RE_HOST = r"(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
_RE_PORT = r"(?P<port>\d{1,5})"
_RE_USERNAME = r"(?P<username>[a-zA-Z0-9._-]+)"
_RE_PASSWORD = r"(?P<password>[a-zA-Z0-9._-]+)"
_RE_SEPARATORS = r"[:;@,]"


def _build_regex(*regexs):
    return _RE_SEPARATORS.join(regexs)


_RE_ADDRESS = _build_regex(_RE_HOST, _RE_PORT)
_RE_ADDRESS_WITH_AUTH = _build_regex(_RE_USERNAME, _RE_PASSWORD, _RE_ADDRESS)
_RE_ADDRESS_WITH_AUTH_REVERSED = _build_regex(_RE_ADDRESS, _RE_USERNAME,
                                              _RE_PASSWORD)


def parse_line(line):
    for regex in [_RE_ADDRESS_WITH_AUTH_REVERSED, _RE_ADDRESS_WITH_AUTH,
                  _RE_ADDRESS]:
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
        return f"Proxy({self.compact})"

    def __repr__(self):
        return f"Proxy({self.compact})"

    def is_authenticated(self):
        return self.username is not None and self.password is not None

    @property
    def compact(self):
        scheme = self.scheme.lower()
        auth = ""
        if self.is_authenticated():
            auth = f"{self.username}:{self.password}@"
        return f"{scheme}://{auth}{self.host}:{self.port}"


class ProxyAdaper(BaseProxy):
    def as_requests(self):
        return {"http": self.compact, "https": self.compact}

    def as_httpx(self):
        return {"http://": self.compact, "https://": self.compact}

    def as_httpx_line(self):
        return self.compact

    def as_pyrogram(self):
        return {"scheme": self.scheme,
                "hostname": self.host,
                "port": self.port,
                "username": self.username,
                "password": self.password}


class Proxy(ProxyAdaper):
    @classmethod
    def from_line(cls, line, default_scheme="http"):
        if not (attrs := parse_line(line)):
            raise ValueError("failed to parse line")

        host = attrs.get("host")
        port = attrs.get("port")
        scheme = attrs.get("scheme", default_scheme)
        username = attrs.get("username")
        password = attrs.get("password")
        return cls(host, port, scheme, username, password)


class UnityProxy:
    def __init__(self):
        self.proxies = []

    @classmethod
    def from_file(cls, file, default_scheme="http"):
        filename = os.fsdecode(file)

        def is_format(f):
            f = f.lower()
            if format == f:
                return True

            if filename:
                return filename.lower().endswith(f".{f}")
            return False

        proxies = []

        if is_format("txt"):
            with open(file) as f:
                for line in f:
                    proxy = Proxy.from_line(line.strip(), default_scheme)
                    proxies.append(proxy)

        elif is_format("json"):
            with open(file) as f:
                data = json.load(f)

            if not isinstance(data, (list, tuple)):
                raise ValueError(f"could not parse file: {file}")

            for item in data:
                host = item.get("host") or item.get("ip")
                port = item.get("port")
                scheme = item.get("scheme", default_scheme)
                username = item.get("username") or item.get("login")
                password = item.get("password")
                proxies.append(Proxy(host, port, scheme, username, password))

        obj = cls()
        obj.proxies = proxies
        return obj
