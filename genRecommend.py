import pandas as pd
from collections import Counter

data = {
    "sentiment": ["Negative", "Negative", "Positive", "Negative"],
    "aspects": ["battery;comfort", "comfort;price", "design", "software bugs"]
}
df = pd.DataFrame(data)

neg_aspects = []
for _, row in df.iterrows():
    if row['sentiment'] != 'Negative': continue
    aspects = str(row.get('aspects','')).split(';')
    neg_aspects.extend([a.strip().lower() for a in aspects if a.strip()])

aspect_counts = Counter(neg_aspects)
top_neg = aspect_counts.most_common(5)

print("Top negative aspects and recommendations:\n")
for aspect, count in top_neg:
    print(f"- {aspect} ({count} mentions)")
    if "battery" in aspect:
        print("  → Recommendation: Improve battery life.")
    elif "comfort" in aspect:
        print("  → Recommendation: Improve comfort design.")
    elif "price" in aspect:
        print("  → Recommendation: Consider pricing options.")
    elif "software" in aspect or "bug" in aspect:
        print("  → Recommendation: Fix software bugs.")
    else:
        print("  → Recommendation: Investigate further.")