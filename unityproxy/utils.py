import re


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
_RE_ADDRESS_WITH_AUTH_REVERSED = _build_regex(_RE_ADDRESS, _RE_USERNAME, _RE_PASSWORD)


def parse_line(line):
    for regex in [_RE_ADDRESS_WITH_AUTH_REVERSED, _RE_ADDRESS_WITH_AUTH, _RE_ADDRESS]:
        if match := re.search(regex, line):
            attrs = match.groupdict()
            if attrs.get("port"):
                attrs["port"] = int(attrs["port"])

            if match := re.search(_RE_SCHEME, line):
                attrs["scheme"] = match.group(1)

            return attrs
    return {}

