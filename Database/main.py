from fastapi import FastAPI, HTTPException, Depends
from database import SessionLocal,engine
from models import Product
import databasemodels
from sqlalchemy.orm import Session
app = FastAPI()

databasemodels.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

products=[
    Product(id=1, name="samuel", description="works for me", price=20000.0),
    Product(id=2, name="sami", description="works for me", price=23000.0),
]
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = SessionLocal()

    count=db.query(databasemodels.product).count()
    if count > 0:
        db.close()
        return

    for product in products:
        db.add(databasemodels.product(**product.model_dump()))
    db.commit()
    db.close()

init_db()    

@app.get("/products")
def  AllProducts(db: Session = Depends(get_db)):
    # db=SessionLocal()
    products = db.query(databasemodels.product).all()
    db.close()
    return products


@app.post("/product")
def  ADDProduct(pro:Product):
    db = SessionLocal()
    db.add(databasemodels.product(**pro.model_dump()))
    db.commit()
    db.close()
    return "product received"


@app.get("/product/{id}")
def getByID(id: int, db: Session = Depends(get_db)):
    dp_product=db.query(databasemodels.product).filter(databasemodels.product.id==id).first()
    # for product in products:
    #    if product.id ==id:
    #        return product
    if dp_product:
        return dp_product
    else:
       return "Product not found"
    

@app.put("/product/{id}")
def update_product(id: int, updated_product: Product):
    for i, product in enumerate(products):
        if product.id == id:
            products[i] = updated_product
            return {"message": "Product updated successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/product/{id}")
def delete_product(id: int):
    for i, product in enumerate(products):
        if product.id == id:
            del products[i]
            return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")