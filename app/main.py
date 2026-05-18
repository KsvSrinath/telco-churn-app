from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="Telco Churn Predictor API")

# Load model and scaler
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model  = joblib.load(os.path.join(BASE_DIR, "model", "churn_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "model", "scaler.pkl"))

class Customer(BaseModel):
    AccountWeeks:    float
    ContractRenewal: int
    DataPlan:        int
    DataUsage:       float
    CustServCalls:   int
    DayMins:         float
    DayCalls:        int
    MonthlyCharge:   float
    OverageFee:      float
    RoamMins:        float

@app.get("/")
def root():
    return {"status": "✅ Telco Churn API is running"}

@app.post("/predict")
def predict(customer: Customer):
    data   = np.array([[*customer.dict().values()]])
    scaled = scaler.transform(data)
    pred   = model.predict(scaled)[0]
    prob   = model.predict_proba(scaled)[0][1]
    return {
        "churn_prediction":  int(pred),
        "churn_probability": round(float(prob), 4),
        "risk_level": "High 🔴" if prob > 0.7 else "Medium 🟡" if prob > 0.4 else "Low 🟢"
    }