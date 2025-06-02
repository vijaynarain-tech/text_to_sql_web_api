# Text-to-SQL Query System

A natural language to SQL query system powered by Sarvam AI. This application allows users to query a business database using plain English questions.

## Features

- Natural language to SQL query conversion
- Interactive Streamlit UI
- Sample business database with 10 tables
- Real-time query execution and results display
- Schema visualization

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Sarvam AI API key:
   - Create a `.env` file in the project root
   - Add your API key: `SARVAM_API_KEY=Bearer YOUR_API_KEY_HERE`

3. Create the sample database:
```bash
python create_sample_db.py
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Open the application in your web browser
2. View the database schema by clicking on the "Database Schema" expander
3. Enter your question in natural language
4. Click "Generate SQL" to see the generated SQL query and results

## Example Questions

- "What are the top 5 products by sales?"
- "Show me all customers who joined in the last month"
- "What is the total revenue by product category?"
- "List all employees in the sales department"
- "What products are low in stock?"

## Project Structure

- `app.py` - Main Streamlit application
- `create_sample_db.py` - Script to create and populate the sample database
- `requirements.txt` - Project dependencies
- `sample_business.db` - SQLite database file (created after running create_sample_db.py)

## Requirements

- Python 3.7+
- Sarvam AI API key
- Internet connection for API calls

## License

This project is for educational and non-commercial use only. 