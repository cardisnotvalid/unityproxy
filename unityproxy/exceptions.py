class UnityProxyException(Exception):
    def __init__(self, message="An error occurred in UnityProxy"):
        super().__init__(message)


class ProxyParseError(UnityProxyException):
    def __init__(self, line):
        message = f"Failed to parse proxy line: {line}"
        super().__init__(message)
