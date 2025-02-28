import sys
import os
import re
from dotenv import load_dotenv
from config.schema import SCHEMA_CONTEXT  # Shared schema context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Allowed tables and columns for simple validation (if needed)
ALLOWED_TABLES = {"departments", "employees", "orders", "products"}
ALLOWED_COLUMNS = {
    "departments": {"id", "name"},
    "employees": {"id", "name", "department_id", "email", "salary", "employee_name_embedding"},
    "orders": {"id", "customer_name", "employee_id", "order_total", "order_date", "customer_name_embedding"},
    "products": {"id", "name", "price", "product_name_embedding"}
}

def classify_query(natural_query: str) -> str:
    """
    Classify the natural language query as 'SQL_ONLY', 'VECTOR_ONLY', or 'HYBRID'.
    Uses a simple heuristic: if the word 'similar' is present, assume vector or hybrid search.
    Otherwise, assume a pure SQL query.
    """
    query_lower = natural_query.lower()
    if "similar" in query_lower:
        if any(keyword in query_lower for keyword in ["less than", "above", "between", "cost", "price"]):
            return "HYBRID"
        else:
            return "VECTOR_ONLY"
    else:
        return "SQL_ONLY"

def generate_prompt(natural_query: str, schema_context: str, query_type: str) -> str:
    """
    Generate a prompt for the LLM that instructs it to produce a SQL query.
    
    Parameters:
    - natural_query: The user's query in plain language.
    - schema_context: A comprehensive description of the database schema.
    - query_type: One of 'SQL_ONLY', 'VECTOR_ONLY', or 'HYBRID'.
    
    Returns:
    - A prompt string.
    """
    base_instructions = (
        "You are an expert in SQL query generation. Based solely on the provided schema context, "
        "generate a valid PostgreSQL SQL query that exactly answers the user's query. Use parameterized queries where applicable. "
        "Do not include any explanation or commentary in your output."
    )
    
    # Note: Emphasize that for vector similarity search, the operator must be applied to the embedding columns.
    if query_type == "SQL_ONLY":
        additional_instructions = "Generate a pure SQL query without any vector search operators."
    elif query_type == "VECTOR_ONLY":
        additional_instructions = (
            "Generate a SQL query that uses vector similarity search using pgvector operators. "
            "Ensure that vector similarity is applied to the appropriate embedding columns (e.g., use 'product_name_embedding' for products). "
            "Convert the query string to an embedding and compare it with the stored embedding using the '<->' operator."
        )
    elif query_type == "HYBRID":
        additional_instructions = (
            "Generate a SQL query that combines traditional SQL filtering (e.g., using ILIKE, numerical comparisons) "
            "with vector similarity search using pgvector operators. "
            "For vector similarity, ensure you compare the query embedding with the appropriate embedding column (e.g., 'product_name_embedding' for products). "
            "Use the '<->' operator for computing Euclidean distance between vectors."
        )
    else:
        additional_instructions = ""
    
    prompt = (
        f"{base_instructions}\n"
        f"Schema Context:\n{schema_context}\n\n"
        f"User Query: {natural_query}\n\n"
        f"{additional_instructions}"
    )
    return prompt

def call_llm(prompt: str) -> str:
    """
    Call the Groq API with the provided prompt to generate a SQL query.
    
    Returns:
    - The generated SQL query as a string.
    """
    try:
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        client = Groq(api_key=groq_api_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.3,
            max_tokens=500,
            stream=False
        )
        sql_query = completion.choices[0].message.content.strip()
        return sql_query
    except Exception as e:
        print("Error generating SQL query:", e)
        return None

def validate_query(sql_query: str) -> bool:
    """
    Validate the generated SQL query by checking for disallowed keywords.
    
    Returns True if the query appears valid.
    """
    dangerous_keywords = ["drop", "delete", "alter"]
    for word in dangerous_keywords:
        if re.search(r"\b" + word + r"\b", sql_query, re.IGNORECASE):
            return False
    return True

def generate_sql_query(natural_query: str, schema_context: str) -> str:
    """
    Generate a SQL query from a natural language query and schema context.
    This function classifies the query, builds a prompt, calls the LLM, and validates the output.
    
    Returns the generated SQL query or a failure message.
    """
    query_type = classify_query(natural_query)
    prompt = generate_prompt(natural_query, schema_context, query_type)
    sql_query = call_llm(prompt)
    # Return whatever query is generated for further validation.
    return sql_query if sql_query else "Insufficient information provided to generate a SQL query."

if __name__ == "__main__":
    # Example natural language query for testing
    natural_query = "Find products similar to iPhone 13 that cost less than 1000 dollars."
    sql = generate_sql_query(natural_query, SCHEMA_CONTEXT)
    print("Generated SQL Query:")
    print(sql)
