

```markdown
# Natural-Language-Search-For-DB

## 1. Overview

This project demonstrates an end-to-end solution for converting natural language queries into SQL using an LLM. It integrates SQL injection validation and vector-based semantic search (using pgvector) to execute and retrieve data from a PostgreSQL database. A Streamlit UI provides an interactive interface for users to enter queries and view results.

## 2. Project Description

- **LLM-based SQL Query Generation:**  
  Converts user queries into SQL. The system supports pure SQL queries, vector similarity search queries, and hybrid queries that combine both approaches.

- **SQL Injection Validation:**  
  A dedicated module checks generated SQL queries for potential injection vulnerabilities to ensure that only safe queries are executed.

- **Vector Search with pgvector:**  
  Uses pgvector to store text embeddings and perform semantic similarity searches, improving the accuracy of query results.

- **Streamlit UI:**  
  A web-based interface built with Streamlit allows users to enter natural language queries and view results in real time.

## 3. How to Run It

There are two ways to run the project: using Docker or setting it up locally.

### 3.1. Docker Method (Recommended for Easy Deployment)

**Prerequisite:**  
- Docker must be installed on your system.

**Steps:**

1. Build the Docker image (if not already built):

   ```bash
   docker build -t natural-language-search .
   ```

2. Run the Docker container:

   ```bash
   docker run -p 8501:8501 amanmyuserid/natural-language-search:latest
   ```

3. Open your browser and navigate to [http://localhost:8501/](http://localhost:8501/) to access the Streamlit UI.

### 3.2. Local Setup Method

**Prerequisites:**  
- Python 3.9 or above  
- Git  
- A virtual environment tool (e.g., venv)  
- PostgreSQL with pgvector installed  
- Docker is optional for running PostgreSQL

**Steps:**

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/Natural-Language-Search-For-DB.git
   cd Natural-Language-Search-For-DB
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For macOS/Linux
   # venv\Scripts\activate    # For Windows
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**  
   Create a `.env` file in the project root with the following (example):

   ```
   DATABASE_URL=postgres://user:password@host:port/dbname
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the Streamlit App:**

   ```bash
   streamlit run frontend/streamlit_app.py
   ```

6. Open your browser and navigate to [http://localhost:8501/](http://localhost:8501/) to use the UI.

## 4. Project Folder Structure

```
Natural-Language-Search-For-DB/
├── app/
│   ├── database.py             # Manages PostgreSQL connections & initializes the DB schema
│   ├── hybrid_search.py        # Demonstrates combined SQL and vector similarity search queries
│   ├── insert_data.py          # Inserts sample data into the database tables
│   ├── insert_embeddings.py    # Generates and inserts vector embeddings into the database
│   └── run_query.py            # Command-line tool for generating, validating, and executing SQL queries
├── config/
│   ├── schema.py               # Contains the shared DB schema context (SCHEMA_CONTEXT)
│   └── settings.py             # Contains configuration variables (e.g., DATABASE_URL)
├── frontend/
│   └── streamlit_app.py        # Streamlit UI for user interaction
├── models/
│   ├── llm.py                  # Module for generating SQL queries from natural language using an LLM
│   └── sql_injection_validator.py  # Module to validate SQL queries for SQL injection vulnerabilities
├── Dockerfile                  # Dockerfile for building the Docker image
├── docker-compose.yml          # (Optional) Docker Compose configuration
├── requirements.txt            # Python dependencies with versions
├── .env                        # Environment variables (e.g., GROQ_API_KEY, DATABASE_URL)
└── README.md                   # This documentation file
```

Each component is modular, ensuring that the code is easy to maintain, test, and extend.

---
```

