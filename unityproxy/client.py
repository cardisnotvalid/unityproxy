from collections import UserList

from .proxy import Proxy
from .parser import BaseFileParser


class IterableClient(UserList):
    def __init__(self, ignore_parse_errors=True):
        self._ignore_parse_errors = ignore_parse_errors
        self.data = []

    def ignore_parse_errors(method):
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
        parser_cls = BaseFileParser.get_parser(format)
        parser = parser_cls()
        proxies = parser.parse(file, default_scheme, custom_parser)

        obj = cls()
        obj.data = proxies
        return obj
