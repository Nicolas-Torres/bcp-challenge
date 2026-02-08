from fastapi import FastAPI
from pydantic import BaseModel
from backend.agents.crew import run_fraud_analysis
from backend.agents.crew import TransactionVeredict
import uvicorn


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

@app.post("/transaction", response_model=TransactionVeredict)
async def evaluate_transaction(transaction: Transaction):
    """
    Recibe una transacción y lo evalua usando agentes (fiscal, detective, especialista y juez)
    """
    try:
        transaction_data = transaction.model_dump()
        print(transaction_data)

        result = run_fraud_analysis(transaction_data)
        
        return result

    except Exception as e:
        print(f"Error procesando transaccion: {e}")

@app.get("/")
def home():
    return {"status": "online", "system": "BCP Fraud Agents Ready"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)