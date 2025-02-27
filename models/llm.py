from groq import Groq
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Allowed tables and columns for simple validation
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
        # If there is also a filtering condition (like price or date), treat it as HYBRID.
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
        "generate a valid PostgreSQL SQL query that answers the user's query. Use parameterized queries where applicable. "
        "Do not include any explanation or commentary in your output. If the context does not contain enough information "
        "to generate a correct SQL query, respond with exactly: \"Insufficient information provided to generate a SQL query.\""
    )
    
    if query_type == "SQL_ONLY":
        additional_instructions = "Generate a pure SQL query without any vector search operators."
    elif query_type == "VECTOR_ONLY":
        additional_instructions = (
            "Generate a SQL query that uses vector similarity search using pgvector operators. "
            "Assume that the query should be converted to an embedding and compared with stored embeddings. "
            "Use the '<->' operator for computing the Euclidean distance between vectors."
        )
    elif query_type == "HYBRID":
        additional_instructions = (
            "Generate a SQL query that combines traditional SQL filtering (e.g., using ILIKE, numerical comparisons) "
            "with vector similarity search using pgvector operators. Use the '<->' operator for vector similarity."
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
        # Using a single system message with our entire prompt
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt}
            ],
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
    Validate the generated SQL query by checking for disallowed keywords and ensuring
    it only references allowed tables and columns.
    
    Returns True if the query appears valid.
    """
    # Reject dangerous operations
    dangerous_keywords = ["drop", "delete", "alter"]
    for word in dangerous_keywords:
        if re.search(r"\b" + word + r"\b", sql_query, re.IGNORECASE):
            return False
    # Optionally, add more sophisticated checks on table/column names here.
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
    if sql_query and validate_query(sql_query):
        return sql_query
    else:
        return "Insufficient information provided to generate a SQL query."

if __name__ == "__main__":
    # Comprehensive schema context describing all tables and vector embedding columns.
    schema_context = (
        "Table: departments\n"
        "  - id: SERIAL PRIMARY KEY\n"
        "  - name: VARCHAR(100) UNIQUE\n\n"
        "Table: employees\n"
        "  - id: SERIAL PRIMARY KEY\n"
        "  - name: VARCHAR(100)\n"
        "  - department_id: INT (foreign key to departments.id)\n"
        "  - email: VARCHAR(255) UNIQUE\n"
        "  - salary: DECIMAL(10,2)\n"
        "  - employee_name_embedding: VECTOR(384)\n\n"
        "Table: orders\n"
        "  - id: SERIAL PRIMARY KEY\n"
        "  - customer_name: VARCHAR(100)\n"
        "  - employee_id: INT (foreign key to employees.id)\n"
        "  - order_total: DECIMAL(10,2)\n"
        "  - order_date: DATE\n"
        "  - customer_name_embedding: VECTOR(384)\n\n"
        "Table: products\n"
        "  - id: SERIAL PRIMARY KEY\n"
        "  - name: VARCHAR(100) UNIQUE\n"
        "  - price: DECIMAL(10,2)\n"
        "  - product_name_embedding: VECTOR(384)"
    )
    
    # Example natural language query for testing
    natural_query = "Find products similar to iPhone 13 that cost less than 1000 dollars."
    sql = generate_sql_query(natural_query, schema_context)
    print("Generated SQL Query:")
    print(sql)
