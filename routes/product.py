from fastapi import APIRouter, HTTPException
from database import get_db_connection


router = APIRouter()

@router.get("/products")
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    results = cursor.fetchall()
    conn.close()
    return results

@router.post("/products")
def add_product(product: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)",
                   (product["name"], product["price"]))
    conn.commit()
    conn.close()
    return {"message": "Product added successfully"}

@router.put("/{product_id}")
def update_product(product_id: int, product: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name = %s, price = %s WHERE product_id = %s",
                   (product["name"], product["price"], product_id))
    conn.commit()
    conn.close()
    return {"message": "Product updated successfully"}

@router.delete("/{product_id}")
def delete_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete related transactions first
    cursor.execute("DELETE FROM transactions WHERE product_id = %s", (product_id,))
    
    # Then delete product
    cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Product and its transactions deleted successfully"}
