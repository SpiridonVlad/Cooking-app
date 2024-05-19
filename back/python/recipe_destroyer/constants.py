import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()


RECIPE_RETRIEVER_ALLERGENS_API_URL = os.getenv("RECIPE_RETRIEVER_ALLERGENS_API_URL")
if RECIPE_RETRIEVER_ALLERGENS_API_URL is None:
    raise ValueError("Environment variable 'RECIPE_RETRIEVER_ALLERGENS_API_URL' is not set")

RECIPE_RETRIEVER_RATINGS_API_URL = os.getenv("RECIPE_RETRIEVER_RATINGS_API_URL")
if RECIPE_RETRIEVER_RATINGS_API_URL is None:
    raise ValueError("Environment variable 'USER_RETRIEVER_API_URL' is not set")

RECIPE_RETRIEVER_TAGS_API_URL = os.getenv("RECIPE_RETRIEVER_TAGS_API_URL")
if RECIPE_RETRIEVER_TAGS_API_URL is None:
    raise ValueError("Environment variable 'RECIPE_RETRIEVER_TAGS_API_URL' is not set")

RECIPE_RETRIEVER_IMAGES_API_URL = os.getenv("RECIPE_RETRIEVER_IMAGES_API_URL")
if RECIPE_RETRIEVER_IMAGES_API_URL is None:
    raise ValueError("Environment variable 'RECIPE_RETRIEVER_IMAGES_API_URL' is not set")


MAX_TIMEOUT_TIME_SECONDS = 3
MONGO_URI = os.getenv("MONGO_URI","mongodb://localhost:27017/?directConnection=true")

class ErrorCodes(Enum):
    SERVER_ERROR=26300
    RECIPE_NOT_FOUND=26301
    FAILED_DESTROY_RECIPE=26302
    RECIPE_NOT_FOUND_IN_USERS=26303
    RECIPE_NOT_TAGS=26304
    RECIPE_NOT_ALLERGENS=26304
    RECIPE_NOT_RATINGS=26305
    RECIPE_NOT_AUTHOR=26306
    NOT_RESPONSIVE_API=26307
    RECIPE_NOT_THUMBNAIL=26308


