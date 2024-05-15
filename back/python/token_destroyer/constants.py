from enum import Enum


class ErrorCodes(Enum):
    TOKEN_NOT_FOUND = 22000
    FAILED_TO_DELETE_TOKEN = 22001
    FAILED_TO_GET_TOKEN = 22002
    NO_TOKENS_REMOVED = 22003
    FAILED_TO_REMOVE_TOKEN = 22004
    NO_USERS_MATCHED = 22005
    FAILED_TO_UPDATE_USER = 22006
    SERVER_ERROR = 22007
