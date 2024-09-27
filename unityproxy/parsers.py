import re
import os
import csv
import json
from abc import ABC, abstractmethod

from .proxy import Proxy


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


def read_file_decorator(method):
    def wrapper(self, file, *args, **kwargs):
        if not os.path.exists(file):
            raise FileNotFoundError(f"File {file} does not exist.")
        with open(file, "r", encoding="utf-8") as fp:
            return method(self, fp, *args, **kwargs)
    return wrapper


class TextFileParser(BaseFileParser, format_name="txt"):
    @read_file_decorator
    def parse(self, fp, default_scheme, custom_parser=None):
        return [
            Proxy.from_line(line, default_scheme, custom_parser)
            for line in fp
        ]


class JSONFileParser(BaseFileParser, format_name="json"):
    @read_file_decorator
    def parse(self, fp, default_scheme, custom_parser=None):
        return [
            Proxy.from_data(item, default_scheme)
            for item in json.load(fp)
        ]


class CSVFileParser(BaseFileParser, format_name="csv"):
    @read_file_decorator
    def parse(self, fp, default_scheme, custom_parser=None):
        return [
            Proxy.from_data(item, default_scheme)
            for item in csv.DictReader(fp)
        ]
