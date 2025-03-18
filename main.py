from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import Product, User
from schemas import ProductCreate, Product as ProductSchema
from schemas import UserCreate, User as UserSchema
from database import engine, Base, get_db
import jwt
from datetime import datetime, timedelta

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base.metadata.create_all(bind=engine)

def hash_password(password: str):
  return pwd_context.hash(password)

@app.post("/register/", response_model=UserSchema)
def register(user: UserCreate, db: Session = Depends(get_db)):
  hashed_password = hash_password(user.password)
  db_user = User(username=user.username, hashed_password=hashed_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)   # 刷新以確保獲取自動生成的 id
  return db_user

SECRET_KEY = "Sm36wxFa5sgAPq16KuxMRApENOJKc_Qn-ite7SV4twg"

def create_access_token(data: dict, expires_delta: timedelta = None):
  to_encode = data.copy()
  expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
  db_user = db.query(User).filter(User.username == user.username).first()
  if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
    raise HTTPException(status_code=401, detail="Invalid credentials")
  
  access_token = create_access_token(data={"sub": db_user.username, "role": db_user.role})
  return {"access_token": access_token, "token_type": "bearer"}

from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    username: str = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
      raise HTTPException(status_code=401, detail="User not found")
    return user
  except jwt.PyJWTError:
    raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/users/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_current_user)):
  return current_user

@app.get("/admin")
def read_admin_data(current_user: User = Depends(get_current_user)):
  if current_user.role != "admin":
    raise HTTPException(status_code=403, detail="Not enough permissions")
  return {"message": "Welcome, admin"}


@app.post("/products/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
  # 創建產品時不需要指定 id，因為資料庫會自動生成
  db_product = Product(name=product.name, description=product.description, price=product.price)
  db.add(db_product)
  db.commit()
  db.refresh(db_product)   # 刷新以確保獲取自動生成的 id
  return db_product

@app.get("/products/", response_model=list[ProductSchema])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
  products = db.query(Product).offset(skip).limit(limit).all()
  return products

@app.get("/products/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
  product = db.query(Product).filter(Product.id == product_id).first()
  if product is None:
    raise HTTPException(status_code=404, detail="Product not found")
  return product

@app.put("/products/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
  db_product = db.query(Product).filter(Product.id == product_id).first()
  if product is None:
    raise HTTPException(status_code=404, detail="Product not found")
  
  db_product.name = product.name
  db_product.description = product.description
  db_product.price = product.price
  db.commit()
  db.refresh(db_product)
  return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
  db_product = db.query(Product).filter(Product.id == product_id).first()
  if db_product is None:
    raise HTTPException(status_code=404, detail="Product not found")
  
  db.delete(db_product)
  db.commit()
  return {"message": "Product deleted successfully"}