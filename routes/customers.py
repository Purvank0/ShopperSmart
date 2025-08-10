# customers_routes.py
from fastapi import APIRouter, HTTPException
from database import get_db_connection

router = APIRouter()

@router.get("/{customer_id}")
def get_customers(customer_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
    results = cursor.fetchone()
    cursor.close() 
    conn.close()
    if not results:
        raise HTTPException(status_code=404, detail="Customer not found")
    return results

@router.post("/customers")
def add_customer(customer: dict) -> dict[str, str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, email, phone_number, location) VALUES (%s, %s, %s, %s)",
        (
            customer["name"],
            customer["email"],
            customer["phone_number"],
            customer["location"]
        )
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Customer added successfully"}

@router.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = %s, email = %s WHERE customer_id = %s",
                   (customer["name"], customer["email"], customer_id))
    conn.commit()
    conn.close()
    return {"message": "Customer updated successfully"}

@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete related transactions first
    cursor.execute("DELETE FROM transactions WHERE customer_id = %s", (customer_id,))
    
    # Then delete customer
    cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Customer and their transactions deleted successfully"}
