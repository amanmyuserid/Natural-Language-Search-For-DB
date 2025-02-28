import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from sentence_transformers import SentenceTransformer
import psycopg2
from config.settings import DATABASE_URL

# Load the same pre-trained model used for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_connection():
    """Establish a connection to PostgreSQL."""
    return psycopg2.connect(DATABASE_URL)

def hybrid_product_search(query, top_k=5):
    """
    Perform a hybrid search on products using SQL keyword search and vector similarity.
    
    This function converts the user query into a vector embedding and then runs a SQL query that:
      - Filters product names using ILIKE for keyword matching.
      - Computes similarity using the pgvector distance operator (<=>) on the product_name_embedding column.
      - Orders results by the similarity score (higher is better).
    
    Parameters:
    - query (str): User's search input.
    - top_k (int): Number of results to return.
    
    Returns:
    - List of tuples representing matching products.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Convert query to vector embedding
    query_embedding = model.encode(query).tolist()

    # Hybrid search query: combines SQL ILIKE search and vector similarity.
    # Explicitly cast the parameter to vector type using "::vector" so that the <=> operator works.
    hybrid_query = """
    SELECT id, name, price, 
           (1 - (product_name_embedding <=> %s::vector)) AS similarity_score
    FROM products
    WHERE name ILIKE %s
    ORDER BY similarity_score DESC
    LIMIT %s;
    """

    # Execute the query with the embedding, keyword pattern, and limit.
    cur.execute(hybrid_query, (query_embedding, f"%{query}%", top_k))
    results = cur.fetchall()

    cur.close()
    conn.close()
    
    return results

if __name__ == "__main__":
    search_query = input("Enter a product search term: ")
    results = hybrid_product_search(search_query)

    if results:
        print("Search Results:")
        for row in results:
            # row[0]: id, row[1]: name, row[2]: price, row[3]: similarity_score
            print(f"ID: {row[0]}, Name: {row[1]}, Price: ${row[2]:.2f}, Similarity Score: {row[3]:.4f}")
    else:
        print("No similar products found.")
