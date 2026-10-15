import sqlite3

# 1. Create a file called 'company_data.db' to store our data
connection = sqlite3.connect("company_data.db")
cursor = connection.cursor()

# 2. Create 3 empty tables (like 3 empty Excel sheets)
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    name TEXT,
    region TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    category TEXT,
    price REAL,
    cost REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    order_date TEXT
)
""")

# 3. Fill the tables with fake business data
cursor.executemany("INSERT OR REPLACE INTO customers VALUES (?, ?, ?)", [
    (1, 'Aarav Retail', 'South'),
    (2, 'Meera Tech', 'West'),
    (3, 'Vikram Traders', 'North'),
    (4, 'Priya Mart', 'South')
])

cursor.executemany("INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?)", [
    (101, 'Beverages', 150.0, 90.0),
    (102, 'Semiconductors', 4500.0, 3200.0),
    (103, 'Smartphones', 15000.0, 11000.0),
    (104, 'Laptops', 55000.0, 42000.0)
])

cursor.executemany("INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?)", [
    (1001, 1, 101, 50, '2026-08-12'),
    (1002, 2, 102, 10, '2026-09-01'),
    (1003, 1, 103, 25, '2026-09-18'),
    (1004, 3, 104, 5, '2026-10-02'),
    (1005, 4, 101, 100, '2026-10-10'),
    (1006, 2, 104, 8, '2026-10-12')
])

# 4. Save and close
connection.commit()
connection.close()

print("Success! Your company database is ready!")