from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str


class ProductCreate(ProductBase):
    price: float
    in_stock: bool = True
    category_id: int | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool
    category_id: int | None = None

    model_config = ConfigDict(from_attributes=True)
