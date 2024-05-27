from typing import List, Tuple
from pydantic import BaseModel
from repository import UserCollection

user_collection = UserCollection()


class UserProfileData(BaseModel):
    icon: str | None = None
    displayName: str | None = None
    description: str | None = None
    allergens: List[Tuple[int, str]] | None = None


class UserData:
    def __init__(self, data: UserProfileData):
        self.icon = data.icon
        self.displayName = data.displayName
        self.description = data.description
        self.allergens_to_add = []
        self.allergens_to_remove = []
        if data.allergens is not None:
            for action, allergen in data.allergens:
                match action:
                    case 1:
                        self.allergens_to_add.append(allergen)
                    case -1:
                        self.allergens_to_remove.append(allergen)
