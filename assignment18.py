
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



# 1. Load the dataset
df = pd.read_csv("student_data.csv")

# 2. Display original information
print("Original Shape:", df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nData Information:")
print(df.info())

# Keep original number of rows
original_rows = len(df)

# 3a. Standardize names to Title Case
df["Name"] = df["Name"].str.strip().str.title()

# 3b. Remove extra whitespace from City
df["City"] = df["City"].str.strip()

# 3c. Drop rows with missing Score_ML
df = df.dropna(subset=["Score_ML"])

# 3d. Fill missing Score_Pandas with median
pandas_median = df["Score_Pandas"].median()
df["Score_Pandas"] = df["Score_Pandas"].fillna(pandas_median)

# 3e. Remove rows where Age is negative
df = df[df["Age"] >= 0]

# Number of rows removed
removed_rows = original_rows - len(df)

print("\n================================")
print("CLEANED DATA")
print("================================")

print("Cleaned Shape:", df.shape)
print("Rows Removed:", removed_rows)

print("\nCleaned Data:")
print(df)


# ============================================================
# A2. ANALYSIS
# ============================================================

score_columns = [
    "Score_Pandas",
    "Score_Visualization",
    "Score_ML",
    "Score_Regression"
]

# 5. Mean score for each subject for each course
course_scores = df.groupby("Course")[score_columns].mean()

print("\n================================")
print("AVERAGE SCORE BY COURSE")
print("================================")

print(course_scores)


# 6. Top 3 students by total score
df["Total_Score"] = df[score_columns].sum(axis=1)

top_students = df.nlargest(3, "Total_Score")

print("\n================================")
print("TOP 3 STUDENTS")
print("================================")

print(
    top_students[
        ["StudentID", "Name", "Course", "Total_Score"]
    ]
)


# 7. Percentage of students from Lagos
lagos_count = (df["City"].str.lower() == "lagos").sum()
total_students = len(df)

lagos_percentage = (lagos_count / total_students) * 100

print("\n================================")
print("LAGOS STUDENTS")
print("================================")

print(f"Students from Lagos: {lagos_count}")
print(f"Percentage from Lagos: {lagos_percentage:.2f}%")


# ============================================================
# A3. VISUALIZATION
# ============================================================

sns.set_theme(style="whitegrid")


# 8. Bar Chart - Average Score_ML per Course
plt.figure(figsize=(8, 5))

ml_by_course = df.groupby("Course")["Score_ML"].mean()

ml_by_course.plot(kind="bar")

plt.title("Average ML Score per Course")
plt.xlabel("Course")
plt.ylabel("Average ML Score")
plt.xticks(rotation=0)
plt.tight_layout()

plt.show()


# 9. Histogram - Score_Regression
plt.figure(figsize=(8, 5))

plt.hist