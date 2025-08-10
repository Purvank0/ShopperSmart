from fastapi import APIRouter, HTTPException
from database import get_db_connection


router = APIRouter()

@router.get("/transactions")
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions")
    results = cursor.fetchall()
    conn.close()
    return results

@router.post("/transactions")
def add_transaction(tx: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (customer_id, product_id, purchase_date) VALUES (%s, %s, %s)",
                   (tx["customer_id"], tx["product_id"], tx["purchase_date"]))
    conn.commit()
    conn.close()
    return {"message": "Transaction added successfully"}

@router.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, tx: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE transactions SET customer_id = %s, product_id = %s, purchase_date = %s WHERE transaction_id = %s",
                   (tx["customer_id"], tx["product_id"], tx["purchase_date"], transaction_id))
    conn.commit()
    conn.close()
    return {"message": "Transaction updated successfully"}

@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM transactions WHERE transaction_id = %s", (transaction_id,))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()
    return {"message": "Transaction deleted successfully"}
