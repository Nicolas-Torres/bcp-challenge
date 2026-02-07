from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Transaction(BaseModel):
    transaction_id: str
    customer_id: str
    amount: float
    currency: str
    country: str
    chanel: str
    device_id: str
    timestamp: str
    merchant_id: str

@app.post("/transaction")
async def process_transaction(trx: Transaction):
    trx_data = trx.model_dump()
    print(trx_data)
    
    return {
        "status": "success"
    }
