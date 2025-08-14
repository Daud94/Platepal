from pydantic import BaseModel

from app.enums.dish_categories import DishCategory


class MenuSchema(BaseModel):
    category: DishCategory
    name: str
