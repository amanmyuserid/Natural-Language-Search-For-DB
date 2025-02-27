from groq import Groq
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def validate_sql_injection(sql_query: str) -> str:
    """
    Evaluate the provided SQL query for potential SQL injection vulnerabilities using the Groq API.
    
    The function sends a prompt to the LLM asking it to analyze the query for vulnerabilities.
    
    Returns:
    - A string "Safe" if the query appears secure, or "Vulnerable: <brief explanation>" if it is not.
    """
    # System prompt instructs the LLM to evaluate the SQL query for injection vulnerabilities.
    system_prompt = (
        "You are an expert in SQL injection vulnerability analysis. "
        "Evaluate the following SQL query for any potential SQL injection vulnerabilities. "
        "If the query is secure, respond with exactly: 'Safe'. "
        "If the query is vulnerable, respond with exactly: 'Vulnerable: <brief explanation>' with no additional commentary."
    )
    
    # User prompt provides the SQL query to be evaluated.
    user_prompt = f"SQL Query:\n{sql_query}\n\nEvaluate this query for SQL injection vulnerabilities."
    
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
    # Sample SQL query generated from our LLM module (for testing)
    sample_query = (
        "SELECT p1.name, p1.price "
        "FROM products p1 "
        "WHERE p1.price < 1000 "
        "AND p1.name != 'iPhone 13' "
        "ORDER BY p1.product_name_embedding <-> (SELECT product_name_embedding FROM products WHERE name = 'iPhone 13') "
        "LIMIT 10;"
    )
    validation_result = validate_sql_injection(sample_query)
    print("SQL Injection Validation Result:")
    print(validation_result)
