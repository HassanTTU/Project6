# Project6

# Apple Vision Pro Feedback Analysis

This project performs sentiment analysis and aspect extraction on customer reviews of the Apple Vision Pro. It uses OpenAI's GPT-4 mini model to classify each review as Positive, Neutral, or Negative and identify specific product aspects mentioned. The results are visualized and summarized to support product improvement decisions.

---

## 📁 Files

| File                          | Purpose                                                                 |
|-------------------------------|-------------------------------------------------------------------------|
| `sentiment_aspect_analysis.py` | Reads reviews from `feedback.db`, classifies sentiment, extracts aspects, and saves results to `analysis_summary.csv`. |
| `visualize_summary.py`        | Generates bar charts for sentiment distribution and top aspects.       |
| `generate_recommendations.py` | Analyzes negative aspects and prints actionable product recommendations. |

---

## 🧪 Requirements

- Python 3.8+
- OpenAI Python SDK (`pip install openai`)
- pandas, matplotlib (`pip install pandas matplotlib`)
- A valid OpenAI API key stored in `config.py`:
  ```python
  API_KEY = "sk-..."

# Usage

- 1) Change API_KEY placeholder in config.py to your one
- 2) Run `sentiment_aspect_analysis.py`.
- 3) Run `visualize_summary.py`. You will know have a bar graph to analyze.
- 4) Run `generate_recommendations.py` to give you suggestions.