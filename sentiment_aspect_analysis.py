# run_minimal.py
from openai import OpenAI
from config import API_KEY
import sqlite3, os, time, csv

# Change MODEL if you need a different GPT-4 mini variant (e.g., "gpt-4-mini")
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=API_KEY)
DB_PATH = "feedback.db"
OUT_CSV = "analysis_summary.csv"

def load_reviews_from_db(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cur.fetchall()]
    if not tables:
        conn.close(); raise SystemExit("No tables found in feedback.db")
    table = "reviews" if "reviews" in tables else ("feedback" if "feedback" in tables else tables[0])
    cur.execute(f"PRAGMA table_info({table})")
    cols = [r[1] for r in cur.fetchall()]
    text_col = next((c for c in cols if c.lower() in ('review','text','feedback','comment')), cols[0])
    rows = [r[0] for r in cur.execute(f"SELECT [{text_col}] FROM {table}").fetchall() if r[0]]
    conn.close()
    return rows

def call_openai(prompt, max_tokens=150):
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content":prompt}],
        max_tokens=max_tokens,
        temperature=0
    )
    return resp.choices[0].message.content.strip()

def classify(text):
    p = f'Classify this review as exactly one word: Positive, Neutral, or Negative. Return only the label.\n\n"""{text}"""'
    out = call_openai(p, max_tokens=20)
    label = out.splitlines()[0].strip().capitalize()
    if label not in ("Positive","Neutral","Negative"):
        low = out.lower()
        if "positive" in low or "good" in low or "love" in low: return "Positive"
        if "negative" in low or "bad" in low or "disappoint" in low: return "Negative"
        return "Neutral"
    return label

def extract_aspects(text):
    p = f'List short, comma-separated product aspects or features mentioned in this review. If none, return NONE.\n\n"""{text}"""'
    out = call_openai(p, max_tokens=120)
    if not out or out.strip().upper() == "NONE": return []
    parts = [p.strip().lower() for p in out.replace(";",",").split(",") if p.strip()]
    return parts

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        raise SystemExit("feedback.db not found in current folder")
    reviews = load_reviews_from_db(DB_PATH)
    if not reviews:
        print("No reviews found in the DB"); raise SystemExit
    results = []
    for i, r in enumerate(reviews, 1):
        try:
            s = classify(r)
            a = extract_aspects(r)
        except Exception as e:
            s = "Error"
            a = []
            print("OpenAI error:", str(e))
        print(f"\nReview {i}: {r}\nSentiment: {s}\nAspects: {', '.join(a) if a else 'NONE'}")
        results.append({"review": r, "sentiment": s, "aspects": "; ".join(a)})
        time.sleep(0.25)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["review","sentiment","aspects"])
        writer.writeheader()
        writer.writerows(results)
    print("\nSaved results to", OUT_CSV)