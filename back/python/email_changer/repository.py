from pymongo import MongoClient, timeout
from constants import DB_NAME, MONGO_URI, TIMEOUT_LIMIT, ErrorCodes
from datetime import datetime, timezone


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class DBWrapper:
    def __init__(self):
        try:
            self.connection = MongoClient(MONGO_URI)
        except Exception:
            raise Exception(ErrorCodes.DB_CONNECTION_FAILURE.value)

    def update_email(self, user_id: str, email: str) -> None:
        try:
            with timeout(TIMEOUT_LIMIT):
                self.connection.get_database(DB_NAME).user.update_one({"id": user_id},
                                                                      {"$set": {"login.newEmail": email, "updatedAt": datetime.now(timezone.utc)}})
        except Exception:
            raise Exception(ErrorCodes.FAILED_TO_UPDATE_EMAIL.value)

    def check_unique_email(self, email: str) -> bool:
        try:
            with timeout(TIMEOUT_LIMIT):
                query_result = self.connection.get_database(DB_NAME).user.find_one({"$or": [{"email": email},
                                                                                            {"login.newEmail": email}]})
        except Exception:
            raise Exception(ErrorCodes.FAILED_TO_CHECK_UNIQUE_EMAIL.value)
        return query_result is None
