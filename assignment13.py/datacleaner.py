

import pandas as pd


def clean_hr_data(filename):
    df = pd.read_csv(filename)

    # Drop rows where Name or Age is missing
    df = df.dropna(subset=["Name", "Age"])

    # Convert Name to Title Case
    df["Name"] = df["Name"].str.title()

    # Strip leading/trailing whitespace from City
    df["City"] = df["City"].str.strip()

    # Filter out invalid (negative) Age values
    df = df[df["Age"] >= 0]

    # Fill missing Salary values with 0
    df["Salary"] = df["Salary"].fillna(0)

    df.to_csv("cleaned_data.csv", index=False)
    return df


if __name__ == "__main__":
    cleaned = clean_hr_data("messy_data.csv")
    print(f"Cleaned data saved to 'cleaned_data.csv' ({len(cleaned)} rows kept)\n")
    print(cleaned.to_string(index=False))