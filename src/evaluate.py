import joblib
import numpy as np
from sklearn.metrics import classification_report

from data_preprocessing import load_data, preprocess_data

def evaluate_model(threshold=0.35):
    # Load data
    df = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(df)

    # Load trained model
    model = joblib.load("models/fraud_model.pkl")

    # Predict probabilities
    y_probs = model.predict_proba(X_test)[:, 1]

    # Apply custom threshold
    y_pred = (y_probs >= threshold).astype(int)

    # Print results
    print(f"\nEvaluation at threshold = {threshold}")
    print(classification_report(y_test, y_pred, digits=4))

if __name__ == "__main__":
    evaluate_model(threshold=0.35)
