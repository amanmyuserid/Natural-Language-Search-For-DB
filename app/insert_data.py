import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import psycopg2
from config.settings import DATABASE_URL

def get_connection():
    """Establish a database connection."""
    return psycopg2.connect(DATABASE_URL)

def insert_departments():
    """Insert sample department data."""
    conn = get_connection()
    cur = conn.cursor()

    departments = ["HR", "Engineering", "Sales", "Marketing"]
    
    for dept in departments:
        cur.execute("INSERT INTO departments (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (dept,))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Departments inserted successfully.")

def insert_employees():
    """Insert sample employees (without embeddings yet)."""
    conn = get_connection()
    cur = conn.cursor()

    employees = [
        ("Alice Smith", 2, "alice@company.com", 75000.00), 
        ("Bob Johnson", 3, "bob@company.com", 65000.00),
        ("Charlie Brown", 1, "charlie@company.com", 55000.00),
        ("David White", 2, "david@company.com", 72000.00),
        ("Emma Watson", 3, "emma@company.com", 67000.00),
        ("Frank Castle", 1, "frank@company.com", 59000.00),
        ("Grace Lee", 2, "grace@company.com", 77000.00),
        ("Hank Green", 3, "hank@company.com", 63000.00),
        ("Isabel King", 1, "isabel@company.com", 51000.00),
        ("Jack Reacher", 2, "jack@company.com", 74000.00)
    ]

    for name, dept_id, email, salary in employees:
        cur.execute(
            "INSERT INTO employees (name, department_id, email, salary) VALUES (%s, %s, %s, %s) ON CONFLICT (email) DO NOTHING;",
            (name, dept_id, email, salary)
        )
    
    conn.commit()
    cur.close()
    conn.close()
    print("Employees inserted successfully.")

def insert_orders():
    """Insert sample orders (without embeddings yet)."""
    conn = get_connection()
    cur = conn.cursor()

    orders = [
        ("John Doe", 1, 500.00, "2025-02-25"),
        ("Jane Smith", 2, 1200.00, "2025-02-26"),
        ("Michael Lee", 3, 800.00, "2025-02-27"),
        ("Nancy Drew", 4, 950.00, "2025-02-28"),
        ("Oliver Queen", 2, 1800.00, "2025-02-20"),
        ("Peter Parker", 1, 650.00, "2025-02-21"),
        ("Quincy Adams", 3, 920.00, "2025-02-22"),
        ("Rachel Green", 4, 1500.00, "2025-02-23"),
        ("Steve Rogers", 2, 2000.00, "2025-02-24"),
        ("Tony Stark", 3, 3500.00, "2025-02-19"),
        ("Bruce Wayne", 1, 4400.00, "2025-02-18"),
        ("Clark Kent", 2, 2700.00, "2025-02-17"),
        ("Diana Prince", 3, 1600.00, "2025-02-16"),
        ("Barry Allen", 4, 850.00, "2025-02-15"),
        ("Lex Luthor", 2, 5600.00, "2025-02-14")
    ]

    for customer_name, emp_id, total, date in orders:
        cur.execute(
            "INSERT INTO orders (customer_name, employee_id, order_total, order_date) VALUES (%s, %s, %s, %s);",
            (customer_name, emp_id, total, date)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Orders inserted successfully.")

def insert_products():
    """Insert sample product data (without embeddings yet)."""
    conn = get_connection()
    cur = conn.cursor()

    products = [
        ("iPhone 13", 999.99),
        ("MacBook Air", 1299.99),
        ("Samsung Galaxy S21", 799.99),
        ("Sony Headphones", 199.99),
        ("Dell XPS 13", 1099.99),
        ("Apple Watch", 399.99),
        ("Google Pixel 7", 899.99),
        ("Amazon Echo", 149.99),
        ("Bose SoundLink", 349.99),
        ("Microsoft Surface Pro", 1199.99),
        ("Lenovo ThinkPad", 999.99),
        ("HP Spectre x360", 1399.99),
        ("OnePlus 11", 729.99),
        ("Xiaomi Mi 12", 649.99),
        ("Asus ROG Phone", 999.99)
    ]

    for name, price in products:
        cur.execute(
            "INSERT INTO products (name, price) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING;",
            (name, price)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Products inserted successfully.")

if __name__ == "__main__":
    insert_departments()
    insert_employees()
    insert_orders()
    insert_products()
    print("All initial data inserted successfully.")
