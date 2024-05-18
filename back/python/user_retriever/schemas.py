from pydantic import BaseModel


class UserData(BaseModel):
    userId: str
    username: str 
    displayName: str
    icon: str
    roles: int
    ratingAvg: float
    description: str
    recipes: list[str]
    ratings: list[str]


class UserCardData(BaseModel):
    userId: str
    username: str
    displayName: str
    icon: str
    roles: int
    ratingAvg: float


class UserFullData(BaseModel):
    userId: str
    username: str
    displayName: str
    icon: str
    roles: int
    ratingAvg: float
    description: str
    recipes: list[str]
    ratings: list[str]
    email: str
    followsCount: int
    followersCount: int
    allergens: list[str]
    searchHistory: list[str]
    messageHistory: list[str]
    savedRecipes: list[str]


class UserCardsRequestData(BaseModel):
    ids: list[str]