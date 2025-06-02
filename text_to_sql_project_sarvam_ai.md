# 🧠 Text-to-SQL Query System for Business Analytics (Sarvam AI Powered - Web API)

## 📌 Objective
Build a **Web API** that translates **natural language questions** into **SQL queries** and returns the results — powered by **Sarvam AI API**.

## 🎯 Purpose
Allow seamless programmatic access to a Text-to-SQL system via a simple HTTP API. Useful for integrating into tools or dashboards.

## ✅ Deliverables Checklist

- [ ] Extract and document **database schema** metadata (tables, columns, types).
- [ ] Create and populate a **sample database** with **10 tables**, each with **≥ 50 rows**.
- [ ] Implement Text-to-SQL translation using **Sarvam AI API**.
- [ ] Expose a **Web API endpoint** to:
  - Receive natural language question as a query parameter
  - Return generated SQL and execution result as JSON
- [ ] Evaluate translation quality using:
  - `Exact Match Accuracy`
  - `Execution Accuracy`

## 🧰 Tools & Technologies

- **Sarvam AI API** – LLM backend for natural language to SQL
- **FastAPI** – Lightweight web API framework
- **SQLite/PostgreSQL** – Sample relational database
- **Pandas/SQLAlchemy** – Data access and manipulation

## 🔌 Web API Example Endpoint

### `GET /query?text=your_question_here`

**Request Example:**
```
GET /query?text=What is the total revenue last month?
```

**Response Example:**
```json
{
  "question": "What is the total revenue last month?",
  "generated_sql": "SELECT SUM(revenue) FROM sales WHERE date BETWEEN ...",
  "results": [
    {
      "SUM(revenue)": 123456.78
    }
  ]
}
```

No authentication is required for simplicity (suitable for internal/demo use).

## 🧠 Sarvam AI Integration Example

```python
import requests

def question_to_sql(question, schema_description):
    payload = {
        "inputs": {
            "question": question,
            "schema": schema_description
        }
    }
    headers = {"Authorization": "Bearer YOUR_SARVAM_API_KEY"}
    response = requests.post("https://api.sarvam.ai/text-to-sql", json=payload, headers=headers)
    return response.json().get("sql", "")
```

## 🚀 FastAPI App Example

```python
from fastapi import FastAPI, Query
from src.translator import question_to_sql
import sqlite3
import pandas as pd

app = FastAPI()

@app.get("/query")
def get_sql_result(text: str):
    schema_description = "..."  # Define your schema metadata
    sql = question_to_sql(text, schema_description)

    try:
        conn = sqlite3.connect("data/sample.db")
        df = pd.read_sql_query(sql, conn)
        result = df.to_dict(orient="records")
        return {
            "question": text,
            "generated_sql": sql,
            "results": result
        }
    except Exception as e:
        return {"error": str(e)}
```

## 🧪 Evaluation Metrics

- **Exact Match Accuracy** – Checks if generated SQL exactly matches reference.
- **Execution Accuracy** – Checks if the SQL output matches the expected result.

## 📈 Success Criteria

- ≥ **85% execution accuracy** on held-out test questions
- Web API returns correct SQL and query results in JSON
- Easy to adapt to new schemas

## 📚 Data Requirements

Use at least **10 tables**, each with **≥ 50 rows**.


## 🔒 Security Note
This API is **unauthenticated** by design for demo/internal use. Use proper authentication in production.

## 📄 License
This project is for educational and non-commercial use only.
