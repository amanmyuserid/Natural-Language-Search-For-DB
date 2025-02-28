

```markdown
# Natural-Language-Search-For-DB

## 1. Overview

This project demonstrates an end-to-end solution for converting natural language queries into SQL using an LLM. It i

## 2. Project Description

- **LLM-based SQL Query Generation:**
  Converts user queries into SQL. The system supports pure SQL queries, vector similarity search queries, and hybrid

- **SQL Injection Validation:**
  A dedicated module checks for potential SQL injection vulnerabilities, ensuring that only safe queries are execute

- **Vector Search with pgvector:**
  Uses pgvector to store text embeddings and perform semantic similarity searches, improving query accuracy.

- **Streamlit UI:**
  Provides a user-friendly web interface where users can enter natural language queries and view the results in real

## 3. How to Run It

### Prerequisite
- **Docker** must be installed on your system.

### Running the Project

The project is fully Dockerized for easy deployment. To run the application, simply execute:

```bash
docker run -p 8501:8501 amammyuserid/natural-language-search:latest
```

After running the command, open your browser and navigate to:

http://localhost:8501/

You will see the Streamlit UI where you can enter a natural language query to interact with the database.

## 4. Project Folder Structure

Natural-Language-Search-For-DB/
├── app/
│   ├── database.py               # Manages DB connections & initialization
│   ├── hybrid_search.py          # Demonstrates combining SQL + vector search
│   ├── insert_data.py            # Inserts initial data into tables
│   ├── insert_embeddings.py      # Generates & inserts vector embeddings
│   └── run_query.py              # Command-line interface for generating, validating, & executing queries
├── config/
│   └── schema.py                 # Contains the shared DB schema context (SCHEMA_CONTEXT)
├── frontend/
│   └── streamlit_app.py          # Streamlit UI for user interaction
├── models/
│   ├── llm.py                    # Module for generating SQL queries from natural language using an LLM
│   └── sql_injection_validator.py # Module to validate SQL queries for SQL injection vulnerabilities
├── Dockerfile                    # Dockerfile for building the Docker image
├── requirements.txt              # Python dependencies with versions
├── .env                          # Environment variables (e.g., GROQ_API_KEY, DATABASE_URL)
└── README.md                     # This documentation file
```
