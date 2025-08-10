from fastapi import FastAPI
from routes import customer_routes, product_routes, transaction_routes

app = FastAPI(
    title="ShopSmart API",
    description="API for managing customers, products, and transactions in a shop",
    version="1.0.0"
)

# Include routers
app.include_router(customer_routes.router, prefix="/customers", tags=["Customers"])
app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(transaction_routes.router, prefix="/transactions", tags=["Transactions"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the ShopSmart FastAPI Backend"}
