import os
import json

from .proxy import Proxy
from .abc import BaseFileParser


def open_file_decorator(method):
    def wrapper(self, file, *args, **kwargs):
        if not os.path.exists(file):
            raise FileNotFoundError(f"File {file} does not exist.")
        with open(file, "r", encoding="utf-8") as fp:
            return method(self, fp, *args, **kwargs)
    return wrapper


class TextFileParser(BaseFileParser, format_name="txt"):
    @open_file_decorator
    def parse(self, fp, default_scheme, custom_parser=None):
        return [Proxy.from_line(line, default_scheme, custom_parser) for line in fp]


class JSONFileParser(BaseFileParser, format_name="json"):
    @open_file_decorator
    def parse(self, fp, default_scheme, custom_parser=None):
        return [Proxy.from_data(item, default_scheme) for item in json.load(fp)]
