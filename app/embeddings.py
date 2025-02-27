from models.embed_model import model
from app.database import get_connection

def insert_product(name, price):
    """Generate embedding & insert product into database."""
    embedding = model.encode(name).tolist()
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO products (name, price, embedding) VALUES (%s, %s, %s)",
        (name, price, embedding)
    )

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Inserted Product: {name}")
