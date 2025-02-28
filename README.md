

```markdown
# Natural-Language-Search-For-DB

## 1. Overview

This project demonstrates an end-to-end solution for converting natural language queries into SQL using an LLM. It integrates SQL injection validation and vector-based semantic search (using pgvector) to execute and retrieve data from a PostgreSQL database. A Streamlit UI provides an interactive interface for users to enter queries and view results.

## 2. Project Description

- **LLM-based SQL Query Generation:**  
  The system converts user queries into SQL. It supports pure SQL queries, vector similarity search queries, and hybrid queries that combine both approaches.

- **SQL Injection Validation:**  
  A dedicated module checks generated SQL queries for potential injection vulnerabilities to ensure that only safe queries are executed.

- **Vector Search with pgvector:**  
  The project uses pgvector to store text embeddings and perform semantic similarity searches, improving the accuracy of query results.

- **Streamlit UI:**  
  A web-based interface built with Streamlit allows users to enter natural language queries and see the results in real time.

## 3. How to Run It

### Prerequisite
- **Docker** must be installed on your system.

### Running the Project

The project is fully Dockerized for easy deployment. To run the application, simply execute:

```bash
docker run -p 8501:8501 amanmyuserid/natural-language-search:latest
```

After running the command, open your browser and navigate to:

```
http://localhost:8501/
```

You will see the Streamlit UI where you can enter a natural language query to interact with the database.

## 4. Project Folder Structure

```
Natural-Language-Search-For-DB/
├── app/
│   ├── database.py             # Manages DB connections & initialization.
│   ├── hybrid_search.py        # Demonstrates combined SQL and vector similarity search queries.
│   ├── insert_data.py          # Inserts sample data into database tables.
│   ├── insert_embeddings.py    # Generates and inserts vector embeddings into the database.
│   └── run_query.py            # CLI tool for generating, validating, and executing SQL queries.
├── config/
│   ├── schema.py               # Contains the shared database schema context (SCHEMA_CONTEXT).
│   └── settings.py             # Contains configuration variables (e.g., DATABASE_URL).
├── frontend/
│   └── streamlit_app.py        # Streamlit UI for user interaction.
├── models/
│   ├── llm.py                  # Module for generating SQL queries from natural language using an LLM.
│   └── sql_injection_validator.py  # Module to validate SQL queries for injection vulnerabilities.
├── Dockerfile                  # Dockerfile for building the Docker image.
├── docker-compose.yml          # (Optional) Docker Compose configuration.
├── requirements.txt            # Python dependencies with versions.
├── .env                        # Environment variables (e.g., GROQ_API_KEY, DATABASE_URL).
└── README.md                   # This documentation file.
```

Each component is modular, ensuring that the code is easy to maintain, test, and extend.
```
