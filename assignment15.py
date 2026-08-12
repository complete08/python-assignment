

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ---- Step 1: Load data & separate features from target ----
df = pd.read_csv("raw_housing_data.csv")

X = df.drop(columns=["Sold_Quickly"]).copy()
y = df["Sold_Quickly"].copy()

# ---- Step 2: Handle missing numerical data (median imputation) ----
numerical_cols = ["Square_Footage", "Bedrooms", "Age_of_Home"]
imputer = SimpleImputer(strategy="median")
X[numerical_cols] = imputer.fit_transform(X[numerical_cols])

# ---- Step 3: Encode categorical data ----
# Target: Yes/No -> 1/0
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)
print("Target encoding:", dict(zip(label_encoder.classes_, range(len(label_encoder.classes_)))))

# Features: one-hot encode Neighborhood (pd.get_dummies - simplest route per the hint)
X = pd.get_dummies(X, columns=["Neighborhood"], dtype=int)
print("Feature columns after encoding:", X.columns.tolist())

# ---- Step 4: Feature scaling ----
scaler = StandardScaler()
X = scaler.fit_transform(X)

# ---- Final output ----
print("\nFinal scaled feature array X:")
print(X)
print("\nFinal encoded target array y:")
print(y)