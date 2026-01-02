import os
import joblib
from sklearn.ensemble import IsolationForest
from data_preprocessing import load_data, preprocess_data

def train_anomaly():
    df = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(df)

    iso = IsolationForest(
        n_estimators=200,
        contamination=0.002,
        random_state=42
    )

    iso.fit(X_train)

    os.makedirs("models", exist_ok=True)
    joblib.dump(iso, "models/anomaly_model.pkl")
    print("✅ Anomaly model saved")

if __name__ == "__main__":
    train_anomaly()
