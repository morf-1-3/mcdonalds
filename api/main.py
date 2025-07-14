from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
import json
import os

app = FastAPI()



def read_json():
    BASE_DIR = os.path.dirname(__file__)
    DATA_PATH = os.path.join(BASE_DIR, "output.json")
    with open(DATA_PATH,"r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def get_products():
    data = read_json()
    return Response(content=json.dumps(data, ensure_ascii=False, indent=2), media_type="application/json")

@app.get("/products/{product_name}")
def get_product(product_name: str):
    data = read_json()
    for product in data:
        if product["name"].lower() == product_name.lower():
            return JSONResponse(content=product)
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/products/{product_name}/{product_field}")
def get_product_fild(product_name:str, product_field:str):
    data = read_json()
    for product in data:
        if product["name"].lower() == product_name.lower() and product_field in product:
            return JSONResponse(content=product[product_field])
    raise HTTPException(status_code=404, detail="Product or field not found")