from os import fsdecode as _fsdecode
from queue import Queue
from collections import UserList

from .proxy import Proxy
from .parsers import BaseFileParser
from .exceptions import ProxyParseError


class UnityProxy(UserList):
    def __init__(self, proxies=None):
        if proxies is not None and not isinstance(proxies, list):
            raise TypeError("Expected a list of proxies or None")

        self.data = proxies or []

    def add_by_line(self, line, default_scheme="http", custom_parser=None, 
                    ignore_errors=True):
        if not line.strip():
            return

        try:
            proxy = Proxy.from_line(line, default_scheme, custom_parser)
            self.data.append(proxy)
        except Exception as err:
            if not ignore_errors:
                raise err

    def add_by_values(self, host, port, scheme, username, password):
        self.data.append(Proxy(host, port, scheme, username, password))

    def to_queue(self):
        queue = Queue()
        for proxy in self.data:
            queue.put(proxy)
        return queue

    @classmethod
    def from_file(cls, file, format=None, default_scheme="http", custom_parser=None):
        filename = _fsdecode(file)

        def get_file_format(f):
            if format:
                return format.lower()
            extension = filename.split(".")[-1].lower()
            if not extension:
                raise ValueError("Cannot determine file format from filename: "
                                 f"\"{filename}\"")
            return extension

        file_format = get_file_format(file)
        parser = BaseFileParser.get_parser(file_format)()
        proxies = parser.parse(file, default_scheme, custom_parser)

        return cls(proxies)
