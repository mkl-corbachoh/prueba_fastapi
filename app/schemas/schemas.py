from pydantic import BaseModel, EmailStr, ConfigDict

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


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

# ============ USUARIOS ============

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_admin: bool = False

class UserResponse(UserBase):
    id: int
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"