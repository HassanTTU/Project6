# generate_recommendations.py
import pandas as pd
from collections import Counter

CSV_FILE = "analysis_summary.csv"

df = pd.read_csv(CSV_FILE)

# Normalize sentiment
df['sentiment'] = df['sentiment'].astype(str).str.capitalize()

# Collect aspects from negative reviews only
neg_aspects = []
for _, row in df.iterrows():
    if row['sentiment'] != 'Negative': continue
    aspects = str(row.get('aspects','')).split(';')
    neg_aspects.extend([a.strip().lower() for a in aspects if a.strip()])

# Count and rank
aspect_counts = Counter(neg_aspects)
top_neg = aspect_counts.most_common(5)

# Simple recommendation logic
print("Top negative aspects and recommendations:\n")
for aspect, count in top_neg:
    print(f"- {aspect} ({count} mentions)")
    if "battery" in aspect:
        print("  → Recommendation: Improve battery life through firmware optimization or offer extended battery accessories.")
    elif "comfort" in aspect or "fit" in aspect:
        print("  → Recommendation: Redesign headband or padding to reduce pressure and improve long-term comfort.")
    elif "price" in aspect or "cost" in aspect:
        print("  → Recommendation: Consider tiered pricing, bundles, or financing options to improve perceived value.")
    elif "software" in aspect or "bug" in aspect:
        print("  → Recommendation: Prioritize bug fixes and improve stability in next software update.")
    elif "weight" in aspect or "heavy" in aspect:
        print("  → Recommendation: Explore lighter materials or better weight distribution.")
    else:
        print("  → Recommendation: Investigate this aspect further and consider targeted improvements.")