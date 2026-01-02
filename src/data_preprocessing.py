import pandas as pd
from sklearn.model_selection import train_test_split
from feature_engineering import engineer_features

def load_data():
    df = pd.read_csv("data/creditcard.csv")
    return df

def preprocess_data(df):
    # Rename target column (industry naming)
    df = df.rename(columns={"Class": "is_fraud"})

    # Separate features and target
    X = df.drop("is_fraud", axis=1)
    y = df["is_fraud"]

    # Stratified split (VERY IMPORTANT for fraud problems)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    # Feature engineering + scaling
    X_train, X_test = engineer_features(X_train, X_test)

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    df = load_data()

    print("Dataset shape:", df.shape)
    print("\nFraud count (before split):")
    print(df["Class"].value_counts())

    X_train, X_test, y_train, y_test = preprocess_data(df)

    print("\nTrain shape:", X_train.shape)
    print("Test shape:", X_test.shape)
