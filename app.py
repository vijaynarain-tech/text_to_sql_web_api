from fastapi import FastAPI, Query, HTTPException
import sqlite3
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Text-to-SQL Query API",
    description="API that translates natural language questions into SQL queries using Sarvam AI",
    version="1.0.0"
)

# Sarvam AI API configuration
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "Bearer 9265dfae-35c2-41d1-b4c4-7f519587283d")
SARVAM_API_URL = "https://api.sarvam.ai/v1/chat/completions"

@app.get("/")
async def root():
    """
    Root endpoint that provides API information and usage instructions.
    """
    return {
        "message": "Welcome to Text-to-SQL Query API",
        "endpoints": {
            "/": "This help message",
            "/query": "Convert natural language to SQL and get results. Usage: /query?text=your_question",
            "/schema": "Get database schema information",
            "/docs": "Interactive API documentation (Swagger UI)",
            "/redoc": "Alternative API documentation (ReDoc)"
        },
        "example": {
            "url": "http://localhost:8000/query?text=What%20are%20the%20top%205%20products%20by%20sales",
            "description": "Try this example in your browser or using curl"
        }
    }

def get_database_schema():
    """Get the database schema information"""
    conn = sqlite3.connect('sample_business.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = []
    for table in tables:
        table_name = table[0]
        # Get column information
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema_info.append({
            'table': table_name,
            'columns': [{'name': col[1], 'type': col[2]} for col in columns]
        })
    
    conn.close()
    return schema_info

def clean_sql_query(query):
    """Clean up the SQL query by removing markdown formatting and extra whitespace"""
    # Remove markdown code block formatting
    query = query.replace('```sql', '').replace('```', '')
    # Remove extra whitespace and newlines
    query = ' '.join(query.split())
    return query.strip()

def generate_sql_query(natural_language_query, schema_info):
    """Generate SQL query using Sarvam AI"""
    
    # Create schema context
    schema_context = "Database Schema:\n"
    for table_info in schema_info:
        schema_context += f"\nTable: {table_info['table']}\n"
        schema_context += "Columns:\n"
        for col in table_info['columns']:
            schema_context += f"- {col['name']} ({col['type']})\n"
    
    # Prepare the prompt
    system_prompt = """You are a SQL expert. Given a database schema and a natural language question, 
    generate the corresponding SQL query. Only return the SQL query without any explanations or markdown formatting."""
    
    headers = {
        "Authorization": SARVAM_API_KEY,
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "sarvam-m",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{schema_context}\n\nQuestion: {natural_language_query}\n\nGenerate SQL query:"}
        ],
        "temperature": 0.1,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(SARVAM_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            sql_query = result["choices"][0]["message"]["content"].strip()
            return clean_sql_query(sql_query)
        else:
            raise HTTPException(status_code=500, detail=f"Error from Sarvam AI API: {response.status_code}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Sarvam AI API: {str(e)}")

def execute_sql_query(query):
    """Execute SQL query and return results"""
    try:
        conn = sqlite3.connect('sample_business.db')
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing SQL query: {str(e)}")

class QueryResponse(BaseModel):
    question: str
    generated_sql: str
    results: list

@app.get("/query", response_model=QueryResponse)
async def get_sql_result(text: str = Query(..., description="Natural language question to convert to SQL")):
    """
    Convert a natural language question to SQL and return the results.
    
    Parameters:
    - text: The natural language question to convert to SQL
    
    Returns:
    - JSON response containing the original question, generated SQL, and query results
    """
    # Get database schema
    schema_info = get_database_schema()
    
    # Generate SQL query
    sql_query = generate_sql_query(text, schema_info)
    
    # Execute query and get results
    results = execute_sql_query(sql_query)
    
    return {
        "question": text,
        "generated_sql": sql_query,
        "results": results
    }

@app.get("/schema")
async def get_schema():
    """
    Get the database schema information.
    
    Returns:
    - JSON response containing the database schema
    """
    return get_database_schema()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 