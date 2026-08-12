

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---- Step 1: Load the data ----
df = pd.read_csv("weather_data.csv")

# ---- Step 2: Create the 2x2 subplot figure ----
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Monthly Weather Analysis", fontsize=16, fontweight="bold")

# ---- Top-Left: Temperature Trend (Line Plot) ----
axes[0, 0].plot(df["Day"], df["Temperature"], color="tab:red", marker="o", markersize=3)
axes[0, 0].set_title("Temperature over 30 Days")
axes[0, 0].set_xlabel("Day")
axes[0, 0].set_ylabel("Temperature (\u00b0C)")

# ---- Top-Right: Humidity vs. Wind Speed (Scatter, colored by Condition) ----
sns.scatterplot(data=df, x="Humidity", y="WindSpeed", hue="Condition", ax=axes[0, 1])
axes[0, 1].set_title("Humidity vs. Wind Speed")
axes[0, 1].set_xlabel("Humidity (%)")
axes[0, 1].set_ylabel("Wind Speed (km/h)")

# ---- Bottom-Left: Weather Conditions Breakdown (Bar Chart) ----
condition_counts = df["Condition"].value_counts()
color_map = {"Sunny": "#f4c542", "Cloudy": "#9e9e9e", "Rainy": "#4a90d9"}
bar_colors = [color_map.get(cond, "#4a90d9") for cond in condition_counts.index]

axes[1, 0].bar(condition_counts.index, condition_counts.values, color=bar_colors)
axes[1, 0].set_title("Weather Conditions Breakdown")
axes[1, 0].set_xlabel("Condition")
axes[1, 0].set_ylabel("Number of Days")

# ---- Bottom-Right: Temperature Distribution (Histogram) ----
axes[1, 1].hist(df["Temperature"], bins=10, color="tab:blue", edgecolor="black")
axes[1, 1].set_title("Temperature Distribution")
axes[1, 1].set_xlabel("Temperature (\u00b0C)")
axes[1, 1].set_ylabel("Frequency")

# ---- Step 4: Display ----
plt.tight_layout()
plt.show()