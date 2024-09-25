from abc import ABC, abstractmethod


class BaseProxy(ABC):
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


class BaseFileParser(ABC):
    _parsers = {}

    def __init_subclass__(cls, format_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if format_name:
            BaseFileParser._parsers[format_name] = cls

    @classmethod
    def get_parser(cls, format_name):
        if format_name not in cls._parsers:
            raise ValueError(f"Unsupported file format: {format_name}")
        return cls._parsers[format_name]

    @abstractmethod
    def parse(self, fp, default_scheme, custom_parser=None):
        pass
