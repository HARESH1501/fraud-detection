import os
import lightgbm as lgb
import joblib
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc

from data_preprocessing import load_data, preprocess_data

def train_model():
    # Load & preprocess data
    df = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(df)

    # LightGBM model (industry configuration)
    model = lgb.LGBMClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=-1,
        num_leaves=31,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    # Train model
    model.fit(X_train, y_train)

    # Predict probabilities
    y_probs = model.predict_proba(X_test)[:, 1]

    # Evaluation metrics
    roc_auc = roc_auc_score(y_test, y_probs)

    precision, recall, _ = precision_recall_curve(y_test, y_probs)
    pr_auc = auc(recall, precision)

    print(f"ROC-AUC Score : {roc_auc:.4f}")
    print(f"PR-AUC Score  : {pr_auc:.4f}")

    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)

    # Save trained model
    joblib.dump(model, "models/fraud_model.pkl")
    print("✅ Model saved as models/fraud_model.pkl")

if __name__ == "__main__":
    train_model()
