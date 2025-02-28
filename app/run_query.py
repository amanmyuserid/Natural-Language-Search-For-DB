import sys
import os
from dotenv import load_dotenv
import psycopg2
import re

# Ensure our modules are accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.llm import generate_sql_query
from models.sql_injection_validator import validate_sql_injection, clean_query
from config.schema import SCHEMA_CONTEXT
from config.settings import DATABASE_URL

def execute_sql_query(sql_query: str):
    """
    Execute the provided SQL query using psycopg2 and return the fetched results.
    
    Parameters:
    - sql_query (str): The SQL query to execute.
    
    Returns:
    - List of tuples containing the result rows, or None if execution fails.
    """
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql_query)
        results = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        print("Error executing SQL query:", e)
        return None

def fix_query(sql_query: str) -> str:
    """
    Attempt to fix the SQL query if it uses the wrong column for vector similarity.
    In our schema, vector similarity should be applied to 'product_name_embedding', not 'name'.
    This is a heuristic fix.
    """
    # If the query uses "p.name <->" instead of "p.product_name_embedding <->", try to replace it.
    fixed_query = sql_query
    pattern = r"p\.name\s*<->\s*'([^']+)'"
    if re.search(pattern, sql_query, re.IGNORECASE):
        # Replace with the proper subquery using product_name_embedding
        fixed_query = re.sub(
            pattern,
            r"p.product_name_embedding <-> (SELECT product_name_embedding FROM products WHERE name ILIKE '\1')",
            sql_query,
            flags=re.IGNORECASE
        )
    return fixed_query

def main():
    # Load environment variables from .env
    load_dotenv()
    
    # Get natural language query from the user
    natural_query = input("Enter your natural language query: ")
    
    # Generate SQL query using our LLM module
    sql_query = generate_sql_query(natural_query, SCHEMA_CONTEXT)
    print("Generated SQL Query:")
    print(sql_query)
    
    # Clean the generated SQL query to remove markdown formatting
    cleaned_query = clean_query(sql_query)
    
    # Validate the cleaned SQL query for SQL injection vulnerabilities
    validation_result = validate_sql_injection(cleaned_query)
    print("SQL Injection Validation Result:")
    print(validation_result)
    
    # If the query is flagged as safe, attempt to fix any known issues and execute it
    if validation_result.strip().lower() == "safe":
        # Attempt to fix common issues (e.g., wrong column for vector similarity)
        fixed_query = fix_query(cleaned_query)
        print("Fixed SQL Query:")
        print(fixed_query)
        
        print("The query is safe. Executing query...")
        results = execute_sql_query(fixed_query)
        if results is not None:
            print("Query Results:")
            for row in results:
                print(row)
        else:
            print("Failed to execute the query.")
    else:
        print("The generated query is vulnerable. Query execution aborted.")

if __name__ == "__main__":
    main()
