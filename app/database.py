import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import psycopg2
from config.settings import DATABASE_URL

def get_connection():
    """Establish a connection to PostgreSQL."""
    return psycopg2.connect(DATABASE_URL)

def initialize_db():
    """Create all necessary tables with consistent column naming."""
    conn = get_connection()
    cur = conn.cursor()

    # Enable pgvector extension
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # Create Departments Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        );
    """)

    # Create Employees Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            department_id INT REFERENCES departments(id),
            email VARCHAR(255) UNIQUE NOT NULL,
            salary DECIMAL(10,2) NOT NULL,
            employee_name_embedding VECTOR(384) -- Store embeddings for employee names
        );
    """)

    # Create Orders Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            customer_name VARCHAR(100) NOT NULL,
            employee_id INT REFERENCES employees(id),
            order_total DECIMAL(10,2) NOT NULL,
            order_date DATE NOT NULL,
            customer_name_embedding VECTOR(384) -- Store embeddings for customer names
        );
    """)

    # Create Products Table (Renaming `embedding` to `product_name_embedding`)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            price DECIMAL(10,2) NOT NULL,
            product_name_embedding VECTOR(384) -- Store embeddings for product names
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized with consistent column naming.")

if __name__ == "__main__":
    initialize_db()
