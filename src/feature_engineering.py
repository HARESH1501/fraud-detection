import numpy as np
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

def engineer_features(X_train, X_test):
    X_train = X_train.copy()
    X_test = X_test.copy()

    # Log transform Amount
    X_train["Amount_log"] = np.log1p(X_train["Amount"])
    X_test["Amount_log"] = np.log1p(X_test["Amount"])

    # Scale Amount
    X_train["Amount_scaled"] = scaler.fit_transform(X_train[["Amount"]])
    X_test["Amount_scaled"] = scaler.transform(X_test[["Amount"]])

    # Drop raw Amount
    X_train.drop(columns=["Amount"], inplace=True)
    X_test.drop(columns=["Amount"], inplace=True)

    return X_train, X_test
