from fastapi import FastAPI, HTTPException

from models import Product

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

products=[
    Product(id=1, name="samuel", description="works for me", price=20000.0),
    Product(id=2, name="sami", description="works for me", price=23000.0),
]


@app.get("/products")
def  AllProducts():
    return products


@app.post("/product")
def  ADDProduct(pro:Product):
    products.append(pro)
    return "product received"


@app.get("/product/{id}")
def getByID(id:int):
    for product in products:
       if product.id ==id:
           return product

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