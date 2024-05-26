from constants import ErrorCodes


class ProfileDataChangerException(Exception):
    def __init__(self, status_code: int, error_code: ErrorCodes):
        self.status_code = status_code
        self.error_code = error_code
