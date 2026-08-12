

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

FEATURE_COLS = [
    "Size_sqm", "Bedrooms", "Bathrooms", "Distance_to_Island_km",
    "Age_years", "Has_BQ", "Is_Serviced_Estate",
]

# ================= Part 1: Load and Explore =================

# ---- Generate the dataset (150 records) ----
rng = np.random.default_rng(42)
n = 150

size_sqm = np.clip(np.round(rng.normal(180, 70, n), 0), 45, 450)
bedrooms = np.clip(np.round(size_sqm / 55 + rng.normal(0, 0.7, n)), 1, 6).astype(int)
bathrooms = np.clip(np.round(bedrooms * 0.7 + rng.normal(0, 0.5, n)), 1, 5).astype(int)
distance_to_island_km = np.round(rng.uniform(1, 35, n), 1)
age_years = np.round(rng.uniform(0, 30, n), 0)
has_bq = rng.choice([0, 1], size=n, p=[0.55, 0.45])
is_serviced_estate = rng.choice([0, 1], size=n, p=[0.6, 0.4])

price_naira = (
    15_000_000
    + size_sqm * 350_000
    + bedrooms * 3_000_000
    + bathrooms * 2_000_000
    - distance_to_island_km * 800_000
    - age_years * 400_000
    + has_bq * 8_000_000
    + is_serviced_estate * 15_000_000
)
price_naira = price_naira + rng.normal(0, 0.06, n) * price_naira  # ~6% market noise
price_naira = np.round(np.clip(price_naira, 10_000_000, None), -3)

df = pd.DataFrame({
    "Size_sqm": size_sqm,
    "Bedrooms": bedrooms,
    "Bathrooms": bathrooms,
    "Distance_to_Island_km": distance_to_island_km,
    "Age_years": age_years,
    "Has_BQ": has_bq,
    "Is_Serviced_Estate": is_serviced_estate,
    "Price_Naira": price_naira,
})

print("=" * 60)
print("PART 1: LOAD & EXPLORE")
print("=" * 60)
print("\nFirst 5 rows:")
print(df.head())
print("\nShape:", df.shape)
print("\nDescriptive statistics:")
print(df.describe())
print("\nMissing values:")
print(df.isnull().sum())

plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.savefig("correlation_heatmap.png", dpi=110)
plt.show()

# ================= Part 2: Prepare the Data =================
X = df[FEATURE_COLS]
y = df["Price_Naira"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ================= Part 3: Train the Model =================
model = LinearRegression()
model.fit(X_train_scaled, y_train)

print("\n" + "=" * 60)
print("PART 3: MODEL TRAINING")
print("=" * 60)
print(f"\nIntercept: \u20a6{model.intercept_:,.2f}")

coef_table = pd.DataFrame({
    "Feature": FEATURE_COLS,
    "Coefficient": model.coef_,
}).sort_values("Coefficient", key=abs, ascending=False)
print("\nFeature coefficients (standardized scale, sorted by influence):")
print(coef_table.to_string(index=False))

# ================= Part 4: Evaluate the Model =================
y_pred = model.predict(X_test_scaled)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\n" + "=" * 60)
print("PART 4: MODEL EVALUATION")
print("=" * 60)
print(f"\nMAE  (Mean Absolute Error): \u20a6{mae:,.2f}")
print(f"MSE  (Mean Squared Error):  {mse:,.2f}")
print(f"RMSE (Root Mean Sq Error):  \u20a6{rmse:,.2f}")
print(f"R\u00b2 Score:                    {r2:.4f}  ({r2 * 100:.2f}%)")

# ================= Part 5: Visualize - Actual vs Predicted =================
y_test_millions = y_test / 1_000_000
y_pred_millions = y_pred / 1_000_000

plt.figure(figsize=(8, 7))
plt.scatter(y_test_millions, y_pred_millions, alpha=0.7, edgecolor="white", s=60, label="Predictions")

lims = [
    min(y_test_millions.min(), y_pred_millions.min()),
    max(y_test_millions.max(), y_pred_millions.max()),
]
plt.plot(lims, lims, color="red", linestyle="--", linewidth=2, label="Perfect Prediction")

plt.title("Actual vs. Predicted House Prices")
plt.xlabel("Actual Price (\u20a6 Millions)")
plt.ylabel("Predicted Price (\u20a6 Millions)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("actual_vs_predicted.png", dpi=110)
plt.show()

# ================= Part 6: Make Real Predictions =================
new_properties = pd.DataFrame([
    {  # Property A - Luxury
        "Size_sqm": 350, "Bedrooms": 5, "Bathrooms": 4,
        "Distance_to_Island_km": 3, "Age_years": 2,
        "Has_BQ": 1, "Is_Serviced_Estate": 1,
    },
    {  # Property B - Starter Home
        "Size_sqm": 90, "Bedrooms": 2, "Bathrooms": 1,
        "Distance_to_Island_km": 22, "Age_years": 15,
        "Has_BQ": 0, "Is_Serviced_Estate": 0,
    },
], index=["Property A (Luxury)", "Property B (Starter Home)"])[FEATURE_COLS]

new_properties_scaled = scaler.transform(new_properties)
predicted_prices = model.predict(new_properties_scaled)

print("\n" + "=" * 60)
print("PART 6: NEW PROPERTY PREDICTIONS")
print("=" * 60)
for name, price in zip(new_properties.index, predicted_prices):
    print(f"\n{name}: \u20a6{price:,.2f}")