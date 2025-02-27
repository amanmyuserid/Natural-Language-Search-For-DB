import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import psycopg2
from config.settings import DATABASE_URL

def get_connection():
    """Establish a database connection."""
    return psycopg2.connect(DATABASE_URL)

def insert_departments(conn):
    """
    Insert sample department data into the 'departments' table.
    If a department already exists, it will not be inserted again.
    """
    cur = conn.cursor()

    departments = ["HR", "Engineering", "Sales", "Marketing"]

    for department in departments:
        cur.execute(
            "INSERT INTO departments (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
            (department,)
        )

    conn.commit()
    cur.close()
    print("Departments inserted successfully.")

def insert_employees(conn):
    """
    Insert sample employee data into the 'employees' table.
    If an employee's email already exists, the record will not be duplicated.
    """
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

    for name, department_id, email, salary in employees:
        cur.execute(
            """
            INSERT INTO employees (name, department_id, email, salary) 
            VALUES (%s, %s, %s, %s) 
            ON CONFLICT (email) DO NOTHING;
            """,
            (name, department_id, email, salary)
        )

    conn.commit()
    cur.close()
    print("Employees inserted successfully.")

def insert_orders(conn):
    """
    Insert sample order data into the 'orders' table.
    This links orders to employees who handled them.
    """
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

    for customer_name, employee_id, order_total, order_date in orders:
        cur.execute(
            """
            INSERT INTO orders (customer_name, employee_id, order_total, order_date) 
            VALUES (%s, %s, %s, %s);
            """,
            (customer_name, employee_id, order_total, order_date)
        )

    conn.commit()
    cur.close()
    print("Orders inserted successfully.")

def insert_products(conn):
    """
    Insert sample product data into the 'products' table.
    This includes various electronics and gadgets.
    """
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
            """
            INSERT INTO products (name, price) 
            VALUES (%s, %s) 
            ON CONFLICT (name) DO NOTHING;
            """,
            (name, price)
        )

    conn.commit()
    cur.close()
    print("Products inserted successfully.")

if __name__ == "__main__":
    # Establish a single database connection for efficiency
    conn = get_connection()

    try:
        insert_departments(conn)
        insert_employees(conn)
        insert_orders(conn)
        insert_products(conn)
        print("All initial data inserted successfully.")
    finally:
        conn.close()  # Ensure the database connection is closed after all inserts
