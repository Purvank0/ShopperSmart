from pydantic import BaseModel

class Transaction(BaseModel):
    customer_id: int
    product_id: int
    purchase_date: str
