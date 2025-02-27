import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sentence_transformers import SentenceTransformer
import psycopg2
from config.settings import DATABASE_URL

# Load pre-trained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_connection():
    """Establish a connection to PostgreSQL."""
    return psycopg2.connect(DATABASE_URL)

def batch_update_embeddings(table, id_column, text_column, embedding_column):
    """
    Generate embeddings for a given table and update the database.

    Parameters:
    - table (str): Table name.
    - id_column (str): ID column name.
    - text_column (str): Text column for embedding.
    - embedding_column (str): Column to store generated embeddings.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Fetch records where embedding is NULL
    cur.execute(f"SELECT {id_column}, {text_column} FROM {table} WHERE {embedding_column} IS NULL;")
    records = cur.fetchall()

    if not records:
        print(f"No missing embeddings found in {table}.")
        cur.close()
        conn.close()
        return

    # Extract text data
    ids, texts = zip(*records)

    # Generate vector embeddings in batch
    embeddings = model.encode(list(texts)).tolist()

    # Update database with generated embeddings
    for record_id, embedding in zip(ids, embeddings):
        cur.execute(f"UPDATE {table} SET {embedding_column} = %s WHERE {id_column} = %s;", (embedding, record_id))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Embeddings updated successfully in {table}.")

if __name__ == "__main__":
    # Update embeddings for all required tables
    batch_update_embeddings("employees", "id", "name", "employee_name_embedding")
    batch_update_embeddings("orders", "id", "customer_name", "customer_name_embedding")
    batch_update_embeddings("products", "id", "name", "product_name_embedding")
    print("All embeddings generated and updated in the database.")
