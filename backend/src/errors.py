class HttpError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class BadRequestError(HttpError):
    def __init__(self, message):
        super().__init__(message, 400)


class MissingFieldError(BadRequestError):
    def __init__(self, field):
        message = f"Field {field} is required"
        super().__init__(message)


class DuplicatedFieldError(BadRequestError):
    def __init__(self, field, value):
        message = f"Field {field} with {value} already exists"
        super().__init__(message)
