#!/usr/bin/env python

"""."""

import json


class MemsourceHTTPException(Exception):
    """."""

    def __init__(self, result, message):
        error = json.loads(result._content)
        error.update({"httpErrorCode": message})
        self.message = error
        super().__init__(self.message)


class MemsourceHTTPBadRequestException(MemsourceHTTPException):
    """."""

    def __init__(self, result):
        super().__init__(result, "400 - Bad Request")


class MemsourceHTTPNotAuthorizedException(MemsourceHTTPException):
    """."""

    def __init__(self, result):
        super().__init__(result, "401 - Not Authorized")


class MemsourceHTTPForbiddenException(MemsourceHTTPException):
    """."""

    def __init__(self, result):
        super().__init__(result, "403 - Forbidden")


class MemsourceHTTPNotFoundException(MemsourceHTTPException):
    """."""

    def __init__(self, result):
        super().__init__(result, "404 - Not Found")


class MemsourceHTTPMethodNotAllowedException(MemsourceHTTPException):
    """."""

    def __init__(self, result):
        super().__init__(result, "405 - Method Not Allowed")
