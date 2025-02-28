import sys
import os
import re
from dotenv import load_dotenv
from config.schema import SCHEMA_CONTEXT  # Shared schema context
from models.llm import generate_sql_query  # Import generate_sql_query from llm.py

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from groq import Groq

# Load environment variables from .env file
load_dotenv()

def clean_query(sql_query: str) -> str:
    """
    Clean the SQL query string by removing markdown code fences and extra whitespace.
    """
    sql_query = sql_query.replace("```sql", "").replace("```", "")
    return sql_query.strip()

def validate_sql_injection(sql_query: str) -> str:
    """
    Evaluate the provided SQL query for potential SQL injection vulnerabilities using the Groq API.
    
    The system prompt is explicitly configured so that any query containing destructive operations 
    (e.g., DELETE, DROP, ALTER) is flagged as vulnerable.
    
    Returns:
    - "Safe" if the query appears secure.
    - "Vulnerable: <brief explanation>" if the query appears vulnerable.
    """
    cleaned_query = clean_query(sql_query)
    
    system_prompt = (
        "You are an expert in SQL injection vulnerability analysis. "
        "Evaluate the following SQL query for any potential SQL injection vulnerabilities. "
        "Any query that contains destructive operations such as DELETE, DROP, or ALTER must be flagged as vulnerable, regardless of context. "
        "If the query is secure and does not include any dangerous operations, respond with exactly: 'Safe'. "
        "If the query is vulnerable, respond with exactly: 'Vulnerable: <brief explanation>' with no extra commentary."
    )
    
    user_prompt = f"SQL Query:\n{cleaned_query}\n\nEvaluate this query for SQL injection vulnerabilities."
    
    try:
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        client = Groq(api_key=groq_api_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=100,
            stream=False
        )
        result = completion.choices[0].message.content.strip()
        return result
    except Exception as e:
        print("Error validating SQL query for injection vulnerabilities:", e)
        return "Error"

if __name__ == "__main__":
    # Example natural language query for testing a potentially destructive query
    natural_query = "Remove all orders where order_total is less than 100."
    sql_query = generate_sql_query(natural_query, SCHEMA_CONTEXT)
    print("Generated SQL Query:")
    print(sql_query)
    
    # Validate the generated query for SQL injection vulnerabilities
    validation_result = validate_sql_injection(sql_query)
    print("SQL Injection Validation Result:")
    print(validation_result)
