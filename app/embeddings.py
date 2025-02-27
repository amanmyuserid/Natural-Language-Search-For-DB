from sentence_transformers import SentenceTransformer
import psycopg2
from config.settings import DATABASE_URL

# Load pre-trained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_connection():
    """Establish a connection to PostgreSQL."""
    return psycopg2.connect(DATABASE_URL)

def update_employee_embeddings():
    """Generate embeddings for employee names and update the database."""
    conn = get_connection()
    cur = conn.cursor()

    # Fetch all employee names
    cur.execute("SELECT id, name FROM employees WHERE name_embedding IS NULL;")
    employees = cur.fetchall()

    for emp_id, name in employees:
        embedding = model.encode(name).tolist()
        cur.execute("UPDATE employees SET name_embedding = %s WHERE id = %s;", (embedding, emp_id))

    conn.commit()
    cur.close()
    conn.close()
    print("Employee embeddings updated successfully.")

def update_customer_embeddings():
    """Generate embeddings for customer names and update the database."""
    conn = get_connection()
    cur = conn.cursor()

    # Fetch all customer names
    cur.execute("SELECT id, customer_name FROM orders WHERE customer_embedding IS NULL;")
    customers = cur.fetchall()

    for order_id, name in customers:
        embedding = model.encode(name).tolist()
        cur.execute("UPDATE orders SET customer_embedding = %s WHERE id = %s;", (embedding, order_id))

    conn.commit()
    cur.close()
    conn.close()
    print("Customer embeddings updated successfully.")

def update_product_embeddings():
    """Generate embeddings for product names and update the database."""
    conn = get_connection()
    cur = conn.cursor()

    # Fetch all product names
    cur.execute("SELECT id, name FROM products WHERE embedding IS NULL;")
    products = cur.fetchall()

    for prod_id, name in products:
        embedding = model.encode(name).tolist()
        cur.execute("UPDATE products SET embedding = %s WHERE id = %s;", (embedding, prod_id))

    conn.commit()
    cur.close()
    conn.close()
    print("Product embeddings updated successfully.")

if __name__ == "__main__":
    update_employee_embeddings()
    update_customer_embeddings()
    update_product_embeddings()
    print("All embeddings generated and updated in the database.")
