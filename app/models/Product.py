from pydantic import BaseModel, PositiveInt, PositiveFloat


class Product(BaseModel):
    product_id: PositiveInt
    name: str
    category: str
    price: PositiveFloat
