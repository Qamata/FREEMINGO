from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd

def train_model():
    # Placeholder training pipeline
    data = pd.read_csv("data/sample_data.csv")
    X = data.drop("target", axis=1)
    y = data["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model
