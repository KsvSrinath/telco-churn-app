import streamlit as st, requests

st.set_page_config(page_title="Telco Churn Predictor", page_icon="📡")
st.title("📡 Telco Customer Churn Predictor")
st.markdown("Fill in customer details to predict churn risk.")

col1, col2 = st.columns(2)
with col1:
    account_weeks    = st.slider("Account Weeks",     1, 243, 100)
    data_usage       = st.number_input("Data Usage (GB)", 0.0, 20.0, 1.0)
    cust_serv_calls  = st.slider("Customer Service Calls", 0, 10, 2)
    day_mins         = st.number_input("Day Minutes",  0.0, 400.0, 180.0)
    day_calls        = st.slider("Day Calls",          0, 165, 100)
with col2:
    monthly_charge   = st.number_input("Monthly Charge ($)", 0.0, 120.0, 60.0)
    overage_fee      = st.number_input("Overage Fee ($)",    0.0, 20.0, 5.0)
    roam_mins        = st.number_input("Roam Minutes",       0.0, 100.0, 10.0)
    contract_renewal = st.selectbox("Contract Renewal", [0, 1])
    data_plan        = st.selectbox("Data Plan",        [0, 1])

API_URL = "http://127.0.0.1:8000/predict"  # ← replace after deploy

if st.button("🔍 Predict Churn"):
    payload = {
        "AccountWeeks": account_weeks, "ContractRenewal": contract_renewal,
        "DataPlan": data_plan, "DataUsage": data_usage,
        "CustServCalls": cust_serv_calls, "DayMins": day_mins,
        "DayCalls": day_calls, "MonthlyCharge": monthly_charge,
        "OverageFee": overage_fee, "RoamMins": roam_mins
    }
    res  = requests.post(API_URL, json=payload).json()
    prob = res['churn_probability']
    st.metric("Churn Probability", f"{prob*100:.1f}%")
    st.success(f"Risk Level: {res['risk_level']}")
    st.progress(prob)