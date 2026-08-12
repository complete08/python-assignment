

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

FEATURE_COLS = ["Annual_Spend_Naira", "Monthly_Orders", "Avg_Order_Value", "Returns_Rate"]

# ================= Part 1: Explore & Prepare the Data =================
df = pd.read_csv("customer_data.csv")

print("=" * 60)
print("PART 1: EXPLORE & PREPARE")
print("=" * 60)
print("\nFirst 5 rows:")
print(df.head())
print("\nShape:", df.shape)
print("\nDescriptive statistics:")
print(df.describe())

print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Handle missing values: fill numeric feature gaps with the column median
for col in FEATURE_COLS:
    if df[col].isnull().any():
        df[col] = df[col].fillna(df[col].median())

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# Scale features - drop CustomerID first, it's an identifier, not a feature
features = df[FEATURE_COLS]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# ================= Part 2: Find the Optimal K (Elbow Method) =================
print("\n" + "=" * 60)
print("PART 2: ELBOW METHOD")
print("=" * 60)

inertias = []
k_values = range(1, 9)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    print(f"K={k}: inertia={kmeans.inertia_:.1f}")

plt.figure(figsize=(8, 5))
plt.plot(list(k_values), inertias, marker="o")
plt.title("Elbow Method for Optimal K")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.xticks(list(k_values))
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("elbow_curve.png", dpi=110)
plt.show()

# Inertia drops sharply from K=1 to K=3, then flattens out noticeably from
# K=3 onward (diminishing returns past that point) - the "elbow" is at K=3.
# This also lines up with the business context: ShopNaija wants exactly
# 3 segments (Premium, Regular, Budget), so K=3 is the optimal choice.
OPTIMAL_K = 3

# ================= Part 3: Apply K-Means with Optimal K =================
final_kmeans = KMeans(n_clusters=OPTIMAL_K, random_state=42, n_init=10)
df["Segment"] = final_kmeans.fit_predict(X_scaled)  # added to the ORIGINAL unscaled df

# ================= Part 4: Analyze & Name the Segments =================
print("\n" + "=" * 60)
print("PART 4: SEGMENT ANALYSIS")
print("=" * 60)

segment_summary = df.groupby("Segment")[FEATURE_COLS].mean().round(2)
print("\nSegment summary (mean values):")
print(segment_summary)

# Rank clusters by average spend to map arbitrary cluster IDs to business labels
spend_ranking = segment_summary["Annual_Spend_Naira"].sort_values(ascending=False)
label_by_rank = ["Premium", "Regular", "Budget"]
segment_labels = {seg_id: label_by_rank[rank] for rank, seg_id in enumerate(spend_ranking.index)}

df["Segment_Label"] = df["Segment"].map(segment_labels)

print("\nSegment interpretation:")
for seg_id, label in sorted(segment_labels.items()):
    row = segment_summary.loc[seg_id]
    print(
        f"  Cluster {seg_id} -> {label} Customers "
        f"(avg spend \u20a6{row['Annual_Spend_Naira']:,.0f}, "
        f"{row['Monthly_Orders']:.1f} orders/mo, "
        f"{row['Returns_Rate']:.1%} returns)"
    )

# ================= Part 5: Visualize the Segments =================
plt.figure(figsize=(9, 6))
colors = {"Premium": "#d4af37", "Regular": "#4a90d9", "Budget": "#9e9e9e"}

for label in label_by_rank:
    subset = df[df["Segment_Label"] == label]
    plt.scatter(
        subset["Annual_Spend_Naira"],
        subset["Monthly_Orders"],
        label=label,
        color=colors[label],
        alpha=0.75,
        edgecolor="white",
        s=60,
    )

plt.title("ShopNaija Customer Segments")
plt.xlabel("Annual Spend (\u20a6)")
plt.ylabel("Monthly Orders")
plt.legend(title="Segment")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("customer_segments_scatter.png", dpi=110)
plt.show()