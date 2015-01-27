class BingError(Exception):
    pass


class BingMethodNotImplemented(BingError, NotImplementedError):
    pass


class BingInvalidParameter(BingError):
    pass


class BingAuthorizationError(BingError):
    pass
