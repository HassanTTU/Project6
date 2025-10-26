# visualize_summary.py
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os

IN_CSV = "analysis_summary.csv"
OUT_SENT_PNG = "sentiment_distribution.png"
OUT_ASP_PNG = "aspect_frequency.png"

df = pd.read_csv(IN_CSV)

# Normalize sentiment labels
df['sentiment'] = df['sentiment'].astype(str).str.capitalize()
sent_order = ['Positive','Neutral','Negative']
sent_counts = df['sentiment'].value_counts().reindex(sent_order).fillna(0)

plt.figure(figsize=(6,4))
colors = ['#2ca02c','#ffcc00','#d62728']
sent_counts.plot(kind='bar', color=colors)
plt.title('Sentiment Distribution')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(OUT_SENT_PNG)
plt.close()

# Aspect frequency (aspects are semicolon-separated)
all_aspects = []
for a in df['aspects'].fillna(''):
    if not a: continue
    parts = [p.strip().lower() for p in a.split(';') if p.strip()]
    all_aspects.extend(parts)

asp_counts = Counter(all_aspects)
top = asp_counts.most_common(25)

if top:
    labels, vals = zip(*top)
    plt.figure(figsize=(8,6))
    plt.barh(labels[::-1], vals[::-1], color='#1f77b4')
    plt.title('Top 25 Mentioned Aspects')
    plt.tight_layout()
    plt.savefig(OUT_ASP_PNG)
    plt.close()

print("Sentiment counts:", sent_counts.to_dict())
print("\nTop 10 aspects:")
for k,v in top[:10]:
    print(f"{k}: {v}")
print(f"\nSaved: {OUT_SENT_PNG}, {OUT_ASP_PNG}")