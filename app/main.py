from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI()

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

@app.get("/product/{product_id}")
async def get_product(product_id: int):
    product = next((product for product in sample_products if product["product_id"] == product_id), None)
    if product:
        return product
    else:
        return {"error": "Product not found"}
    
@app.get("/products/search")
async def search_products(
    keyword: str = Query(..., description="Keyword for product search"),
    category: Optional[str] = Query(None, description="Category to filter products by"),
    limit: Optional[int] = Query(10, description="Limit on the number of returned products")
):
    # Filtering product by key word and category
    filtered_products = [
        product for product in sample_products
        if keyword.lower() in product["name"].lower() and (category is None or product["category"].lower() == category.lower())
    ]
    
    # Limited number of product
    return filtered_products[:limit]
