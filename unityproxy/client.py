import os
from collections import UserList

from .proxy import Proxy
from .parser import BaseFileParser


def ignore_parse_errors(method):
    def wrapper(self, *args, **kwargs):
        if self._ignore_parse_errors:
            try:
                method(self, *args, **kwargs)
            except: pass
        else:
            method(self, *args, **kwargs)
    return wrapper


class IterableClient(UserList):
    def __init__(self, ignore_parse_errors=True):
        self._ignore_parse_errors = ignore_parse_errors
        self.data = []

    @ignore_parse_errors
    def add_by_line(self, line, default_scheme="http", custom_parser=None):
        self.data.append(Proxy.from_line(line, default_scheme, custom_parser))

    @ignore_parse_errors
    def add_by_values(self, host, port, scheme, username, password):
        self.data.append(Proxy(host, port, scheme, username, password))

    @classmethod
    def from_file(cls, file, format=None, default_scheme="http", custom_parser=None):
        filename = os.fsdecode(file)

        def determine_format(f):
            if format:
                return format.lower()
            return filename.split(".")[-1].lower()

        parser = BaseFileParser.get_parser(determine_format(file))
        proxies = parser().parse(file, default_scheme, custom_parser)

        obj = cls()
        obj.data = proxies
        return obj
