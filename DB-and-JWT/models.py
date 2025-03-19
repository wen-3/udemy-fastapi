from sqlalchemy import Column, Integer, String
from database import Base

class Product(Base):
  __tablename__ = "products"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  description = Column(String)
  price = Column(Integer)

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  hashed_password = Column(String)
  role = Column(String, default="user")  # 用於角色管理，默認為普通用戶