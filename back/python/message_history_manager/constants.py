import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 8000)
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
USER_RETRIEVER_API_URL = os.getenv("USER_RETRIEVER_API_URL", "http://0.0.0.0:8000")
USER_CARDS_ROUTE = os.getenv("USER_CARDS_ROUTE", "/user-cards")

MAX_TIMEOUT_TIME_SECONDS = 3


class ErrorCodes(Enum):
    SERVER_ERROR = 20800
    MESSAGE_HISTORY_NOT_FOUND = 20801
    DB_CONNECTION_TIMEOUT = 20902
    DB_CONNECTION_FAILURE = 20903
    USER_NOT_FOUND = 20904
