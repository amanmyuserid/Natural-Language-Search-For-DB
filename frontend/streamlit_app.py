import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.schema import SCHEMA_CONTEXT
from config.settings import DATABASE_URL
from models.llm import generate_sql_query
from models.sql_injection_validator import validate_sql_injection, clean_query

load_dotenv()

def execute_sql_query(sql_query: str):
    """
    Execute the provided SQL query using psycopg2 and return the fetched results.
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
        return f"Something went wrong: {e}"

# Large, centered title
st.markdown(
    "<h1 style='text-align: center; font-size: 2.4rem;'>Natural Language SQL Query Interface</h1>",
    unsafe_allow_html=True
)

# Create two columns for layout
left_col, right_col = st.columns(2)

with left_col:
    # Title for the left column
    st.markdown("<h3>Enter your natural language query:</h3>", unsafe_allow_html=True)
    user_query = st.text_area("", height=100)
    run_button = st.button("Run Query")

with right_col:
    # Title for the right column
    st.markdown("<h3>Results</h3>", unsafe_allow_html=True)

if run_button:
    if user_query.strip() == "":
        with right_col:
            st.warning("Please enter a natural language query.")
    else:
        # Generate the SQL query from the LLM
        sql_query = generate_sql_query(user_query, SCHEMA_CONTEXT)
        cleaned_query = clean_query(sql_query)
        
        # Validate the query for SQL injection
        validation_result = validate_sql_injection(cleaned_query)
        
        with right_col:
            if validation_result.strip().lower() == "safe":
                # Execute the query if safe
                results = execute_sql_query(cleaned_query)
                if isinstance(results, str) and results.startswith("Something went wrong"):
                    st.error(results)  # e.g. "Something went wrong: <error>"
                else:
                    if results:
                        st.write(results)
                    else:
                        st.write("No results found.")
            else:
                st.error("The generated query is vulnerable. Query execution aborted.")
