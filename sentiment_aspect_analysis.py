# run_minimal.py
from openai import OpenAI
from config import API_KEY
import sqlite3, os, time

client = OpenAI(api_key=API_KEY)
DB_PATH = "feedback.db"

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

def call_openai(prompt):
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"user","content":prompt}],
        max_tokens=150,
        temperature=0
    )
    return resp.choices[0].message.content.strip()

def classify(text):
    p = f'Classify this review as Positive, Neutral, or Negative and return only the label.\n\n"""{text}"""'
    return call_openai(p).splitlines()[0].strip().capitalize()

def extract_aspects(text):
    p = f'List comma-separated product aspects mentioned. If none, return NONE.\n\n"""{text}"""'
    out = call_openai(p)
    if out.strip().upper() == "NONE":
        return []
    return [s.strip().lower() for s in out.replace(";",",").split(",") if s.strip()]

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        raise SystemExit("feedback.db not found in current folder")
    reviews = load_reviews_from_db(DB_PATH)
    if not reviews:
        print("No reviews found in the DB"); raise SystemExit
    # Process only the first 5 reviews to start (quick, low-cost)
    for i, r in enumerate(reviews[:5], 1):
        try:
            s = classify(r)
            a = extract_aspects(r)
        except Exception as e:
            s = "Error"
            a = []
            print("OpenAI error:", str(e))
        print(f"\nReview {i}: {r}\nSentiment: {s}\nAspects: {', '.join(a) if a else 'NONE'}")
        time.sleep(0.25)