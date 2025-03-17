from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Product
from schemas import ProductCreate, Product as ProductSchema
from database import engine, Base, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)

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