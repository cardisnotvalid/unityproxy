from .parser import parse_line


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


class ProxyAdapter(BaseProxy):
    def as_requests(self):
        return {"http": self.uri, "https": self.uri}

    def as_httpx(self):
        return {"http://": self.uri, "https://": self.uri}

    def as_httpx_line(self):
        return self.uri

    def as_pyrogram(self):
        return {"scheme": self.scheme,
                "hostname": self.host,
                "port": self.port,
                "username": self.username,
                "password": self.password}


class Proxy(ProxyAdapter):
    @classmethod
    def from_data(cls, data, default_scheme="http"):
        return cls(host=data.get("host"),
                   port=data.get("port"),
                   scheme=data.get("scheme", default_scheme),
                   username=data.get("username"),
                   password=data.get("password"))

    @classmethod
    def from_line(cls, line, default_scheme="http", custom_parser=None):
        if data := parse_line(line):
            return cls.from_data(data, default_scheme)
        raise ValueError("failed to parse line")
