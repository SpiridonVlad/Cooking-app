import os
from enum import Enum, unique

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 7997))
HOST = os.getenv("HOST", "localhost")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")

MAX_TIMEOUT_TIME_SECONDS = 3

AI_API_URL = os.getenv("AI_API_URL", "http://localhost:8003")
AI_RECIPE_TOKENIZER_ROUTE = AI_API_URL + "/tokenize/recipe"

ALLERGEN_MANAGER_API_URL = os.getenv("ALLERGEN_MANAGER_API_URL", "http://localhost:8000")
POST_ALLERGENS_ROUTE = ALLERGEN_MANAGER_API_URL + "/"

TAG_MANAGER_API_URL = os.getenv("TAG_MANAGER_API_URL", "http://localhost:8001")
POST_TAGS_ROUTE = TAG_MANAGER_API_URL + "/"

ALLOWED_TAGS = {"p", "ul", "li", "ol", "img", "s", "u", "strong", "em", "br"}
ALLOWED_ATTRIBUTES = {"img": {"src"}}
URL_SCHEMES = {"https", "http"}
UNSAFE_RECIPE_DATA_FIELDS = {"description", "steps"}


class UserRoles:
    VERIFIED = 0b1
    ADMIN = 0b10
    PREMIUM = 0b100
    BANNED = 0b1000
    ACTIVE = 0b0


@unique
class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 26200
    DB_CONNECTION_TIMEOUT = 26201
    DB_CONNECTION_NONTIMEOUT = 26202
    NOT_RESPONSIVE_API = 26203
    NOT_AUTHENTICATED = 26204
    INVALID_TITLE_SIZE = 26205
    INVALID_DESCRIPTION_SIZE = 26206
    INVALID_PREPTIME = 26207
    EMPTY_LIST_STEPS = 26208
    EMPTY_LIST_INGREDIENTS = 26209
    INVALID_THUMBNAIL_URL_SIZE = 26210
    NONEXISTENT_RECIPE = 26211
    FORBIDDEN_USER = 26212
    MALFORMED_HTML = 26213
    USER_ROLES_INVALID_VALUE = 26214
