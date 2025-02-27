# This file holds the shared schema context for our database.
SCHEMA_CONTEXT = (
    "Table: departments\n"
    "  - id: SERIAL PRIMARY KEY\n"
    "  - name: VARCHAR(100) UNIQUE\n\n"
    "Table: employees\n"
    "  - id: SERIAL PRIMARY KEY\n"
    "  - name: VARCHAR(100)\n"
    "  - department_id: INT (foreign key to departments.id)\n"
    "  - email: VARCHAR(255) UNIQUE\n"
    "  - salary: DECIMAL(10,2)\n"
    "  - employee_name_embedding: VECTOR(384)\n\n"
    "Table: orders\n"
    "  - id: SERIAL PRIMARY KEY\n"
    "  - customer_name: VARCHAR(100)\n"
    "  - employee_id: INT (foreign key to employees.id)\n"
    "  - order_total: DECIMAL(10,2)\n"
    "  - order_date: DATE\n"
    "  - customer_name_embedding: VECTOR(384)\n\n"
    "Table: products\n"
    "  - id: SERIAL PRIMARY KEY\n"
    "  - name: VARCHAR(100) UNIQUE\n"
    "  - price: DECIMAL(10,2)\n"
    "  - product_name_embedding: VECTOR(384)"
)
