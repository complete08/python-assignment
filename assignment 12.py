
import pandas as pd

# ---- Step 2: Load the dataset ----
df = pd.read_csv("employees.csv")

# ---- Step 3: Data Inspection ----
print("=" * 50)
print("DATAFRAME INFO (before cleaning)")
print("=" * 50)
df.info()

# ---- Step 4: Handle missing values ----
# Fill missing Salary with the average (mean) salary
mean_salary = df["Salary"].mean()
df["Salary"] = df["Salary"].fillna(mean_salary)

# Fill missing Join_Date with a default date
df["Join_Date"] = df["Join_Date"].fillna("2023-01-01")

# ---- Step 5: Text cleaning ----
# Strip leading/trailing whitespace from Name
df["Name"] = df["Name"].str.strip()

# ---- Step 6: Filtering ----
# Clean Department column (whitespace) before filtering, same as the Class Task
df["Department"] = df["Department"].str.strip()

it_employees = df[df["Department"] == "IT"]

# ---- Step 7: Save filtered data ----
it_employees.to_csv("it_employees.csv", index=False)

# ---- Verify results ----
print("\n" + "=" * 50)
print("DATAFRAME INFO (after cleaning)")
print("=" * 50)
df.info()

print(f"\nMean salary used to fill gaps: {mean_salary:.2f}")
print(f"Saved {len(it_employees)} IT department employees to 'it_employees.csv'")
print("\nPreview of it_employees.csv:")
print(it_employees.head())