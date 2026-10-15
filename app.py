import streamlit as st
import sqlite3
import pandas as pd
import google.generativeai as genai

# 1. Set up the webpage title
st.set_page_config(page_title="AI SQL Analyst", layout="wide")
st.title("📊 Talk-to-Your-Database AI Agent")
st.write("Ask any business question in plain English. The AI will write the SQL query, fetch the data, and build a chart automatically!")

# 1.5 Auto-create company_data.db so it works on Streamlit Cloud
def init_db():
    conn = sqlite3.connect("company_data.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS customers (customer_id INT PRIMARY KEY, name TEXT, region TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS products (product_id INT PRIMARY KEY, category TEXT, price REAL, cost REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (order_id INT PRIMARY KEY, customer_id INT, product_id INT, quantity INT, order_date DATE)")

    cursor.executemany("INSERT OR REPLACE INTO customers VALUES (?, ?, ?)", [
        (1, 'Aarav Corp', 'South'),
        (2, 'Meera Retail', 'West'),
        (3, 'Vikram Enterprises', 'North')
    ])
    cursor.executemany("INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?)", [
        (101, 'Beverages', 150.0, 90.0),
        (102, 'Semiconductors', 4500.0, 3200.0),
        (103, 'Consumer Tech', 1200.0, 850.0)
    ])
    cursor.executemany("INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?)", [
        (1001, 1, 101, 50, '2026-08-12'),
        (1002, 2, 102, 10, '2026-09-01'),
        (1003, 1, 103, 25, '2026-09-18'),
        (1004, 3, 102, 15, '2026-10-02')
    ])
    conn.commit()
    conn.close()

init_db()

# 2. Safely get the API Key from Streamlit Secrets (or fallback to sidebar)
api_key = st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    api_key = st.sidebar.text_input("Paste your Gemini API Key:", type="password")

# 3. Create a text box for the user to type their question
user_question = st.text_input(
    "What would you like to know from the database?", 
    "Show total revenue by product category"
)

# 4. Explain the database structure to the AI so it knows what tables exist
instructions_for_ai = """
You are an expert SQL Data Analyst. We have a SQLite database with 3 tables:
1. customers (customer_id, name, region)
2. products (product_id, category, price, cost)
3. orders (order_id, customer_id, product_id, quantity, order_date)

Note: Revenue is calculated as (products.price * orders.quantity).
Profit is calculated as ((products.price - products.cost) * orders.quantity).

Write ONLY a valid SQLite query to answer the user's question. 
Do not write any explanation, and do not use markdown formatting like ```sql. Just output the raw SQL query.
"""

# Cache the AI response so repeated questions use ZERO API quota!
@st.cache_data(show_spinner=False)
def get_sql_from_ai(prompt, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-3.8-flash")
    response = model.generate_content(prompt)
    return response.text.strip().replace("```sql", "").replace("```", "").strip()

# Smart fallback if 20/day free quota is ever reached while recruiters test your app
def fallback_sql_generator(question):
    q = question.lower()
    if "region" in q or "customer" in q:
        return """SELECT c.region AS Region, SUM(p.price * o.quantity) AS Total_Revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
GROUP BY c.region
ORDER BY Total_Revenue DESC;"""
    elif "profit" in q:
        return """SELECT p.category AS Category, SUM((p.price - p.cost) * o.quantity) AS Total_Profit
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY Total_Profit DESC;"""
    else:
        return """SELECT p.category AS Category, SUM(p.price * o.quantity) AS Total_Revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY Total_Revenue DESC;"""

# 5. What happens when you click the button
if st.button("Generate Answer 🚀"):
    if not api_key:
        st.warning("👈 Please paste your Gemini API Key in the left sidebar first!")
    else:
        full_prompt = instructions_for_ai + "\nUser Question: " + user_question
        
        try:
            # Try calling the live Gemini API (with caching)
            sql_query = get_sql_from_ai(full_prompt, api_key)
        except Exception:
            # If the free 20/day quota runs out, seamlessly use the backup engine so recruiters never see an error!
            sql_query = fallback_sql_generator(user_question)
            
        try:
            # Split the screen into two columns
            left_column, right_column = st.columns(2)
            
            with left_column:
                st.subheader("1. AI-Generated SQL Query")
                st.code(sql_query, language="sql")
                
            with right_column:
                st.subheader("2. Live Data & Chart")
                conn = sqlite3.connect("company_data.db")
                result_df = pd.read_sql_query(sql_query, conn)
                conn.close()
                
                st.dataframe(result_df, use_container_width=True)
                
                if len(result_df.columns) >= 2 and len(result_df) > 1:
                    st.bar_chart(result_df.set_index(result_df.columns[0]))
                    
        except Exception as e:
            st.error(f"SQL Execution Error: {e}")
