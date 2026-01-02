import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os

def save_scaler():
    df = pd.read_csv("data/creditcard.csv")
    scaler = StandardScaler()
    scaler.fit(df[["Amount"]])
    os.makedirs("models", exist_ok=True)
    joblib.dump(scaler, "models/scaler.pkl")
    print("✅ Scaler saved as models/scaler.pkl")

if __name__ == "__main__":
    save_scaler()
