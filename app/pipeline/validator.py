from pydantic import BaseModel, Field
from typing import List

class ProductSchema(BaseModel):
    title: str = Field(description="The exact title or name of the product.")
    price: float = Field(description="The numeric price value of the product.")
    description: str = Field(description="Product specifications, features, or detailed description.")
    url: str = Field(description="The URL of the product. Leave as empty string if not available.")

class ProductListSchema(BaseModel):
    products: List[ProductSchema] = Field(description="A list containing the extracted product objects.")