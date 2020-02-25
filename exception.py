
class RoiException(Exception):
    pass


class EmptyInputError(RoiException):
    pass


class DataTypeException(RoiException):
    pass


class DataRangeException(RoiException):
    pass


class AuthException(RoiException):
    pass
