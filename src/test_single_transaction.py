import joblib
from data_preprocessing import load_data, preprocess_data

# Load model
model = joblib.load("models/fraud_model.pkl")

# Load & preprocess data
df = load_data()
X_train, X_test, y_train, y_test = preprocess_data(df)

# Pick one LEGIT transaction
legit_sample = X_test[y_test == 0].iloc[0:1]

# Pick one FRAUD transaction
fraud_sample = X_test[y_test == 1].iloc[0:1]

def predict(sample, label):
    prob = model.predict_proba(sample)[0][1]
    pred = "FRAUD" if prob >= 0.35 else "LEGIT"
    print(f"{label} → Probability: {round(prob,4)} | Prediction: {pred}")

predict(legit_sample, "LEGIT")
predict(fraud_sample, "FRAUD")
