from models.embed_model import model
from app.database import get_connection

def search_similar_products(query, top_n=5):
    """Search for products similar to the input query."""
    query_embedding = model.encode(query).tolist()
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT name, price, embedding <=> %s AS similarity
        FROM products
        ORDER BY similarity ASC
        LIMIT %s;
    """, (query_embedding, top_n))

    results = cur.fetchall()
    cur.close()
    conn.close()

    print("\n🔍 Similar Products:")
    for name, price, similarity in results:
        print(f"- {name} (${price}) | Similarity Score: {similarity}")

if __name__ == "__main__":
    search_similar_products("iPhone")
