import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Database se connect karo
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Step 2: Sales table banao agar pehli baar run kar rahe ho
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
''')

# Step 3: Sample data daal do
sample_data = [
    ('Apple', 10, 0.5),
    ('Banana', 5, 0.3),
    ('Apple', 7, 0.5),
    ('Orange', 8, 0.7),
    ('Banana', 10, 0.3),
    ('Orange', 4, 0.7),
]
cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
conn.commit()

# Step 4: Sales ka summary query
query = """
SELECT 
    product, 
    SUM(quantity) AS total_qty, 
    SUM(quantity * price) AS revenue 
FROM sales 
GROUP BY product
"""
df = pd.read_sql_query(query, conn)

# Step 5: Result print karo
print("Sales Summary:")
print(df)

# Step 6: Graph banao
df.plot(kind='bar', x='product', y='revenue', title='Revenue by Product', legend=False)
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.show()

# Step 7: Database connection band karo
conn.close()
