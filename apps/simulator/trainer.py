import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Load dataset
data = pd.read_csv("data/routes.csv")

# 🔥 Remove NaN values (important fix)
data = data.dropna()

X = data[["distance", "traffic"]]
y = data["fuel"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "models/fuel_model.pkl")

print("✅ Model trained successfully!")
