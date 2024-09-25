import json
from functools import wraps
from collections import UserList

from .proxy import Proxy


class IterableUnityProxy(UserList):
    def __init__(self, ignore_parse_errors=True):
        self._ignore_parse_errors = ignore_parse_errors
        self.data = []

    def ignore_parse_errors(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            if self._ignore_parse_errors:
                try:
                    method(self, *args, **kwargs)
                except: pass
            else:
                method(self, *args, **kwargs)
        return wrapper

    @ignore_parse_errors
    def add_by_line(self, line, default_scheme="http", custom_parser=None):
        self.data.append(Proxy.from_line(line, default_scheme, custom_parser))

    @ignore_parse_errors
    def add_by_values(self, host, port, scheme, username, password):
        self.data.append(Proxy(host, port, scheme, username, password))

    @classmethod
    def from_file(cls, file, format="txt", default_scheme="http", custom_parser=None):
        proxies = []

        if format == "txt":
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    proxies.append(Proxy.from_line(line.strip(), default_scheme,
                                                   custom_parser))
        elif format == "json":
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    proxies.append(Proxy.from_data(item))
        else:
            raise ValueError(f"Unsupported file format: {file_format}")

        obj = cls()
        obj.data = proxies
        return obj


class UnityProxy(IterableUnityProxy):
    pass
