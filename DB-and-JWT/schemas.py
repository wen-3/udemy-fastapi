from pydantic import BaseModel

# 用於創建和更新產品的模式
class ProductBase(BaseModel):
  name: str
  description: str
  price: int

# 用於創建產品的模式
class ProductCreate(ProductBase):
  pass

# 用於返回產品的模式(包括 id)
class Product(ProductBase):
  id: int

  class Config:
    orm_mode = True   # 讓 Pydantic 模型能夠與 ORM 模型交互

class UserBase(BaseModel):
  username: str

class UserCreate(UserBase):
  password: str   # 用於註冊時提供密碼

class User(UserBase):
  id: int
  role: str   # 返回用戶時包含角色資訊

  class Config:
    orm_mode = True