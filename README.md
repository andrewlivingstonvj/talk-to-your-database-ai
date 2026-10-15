# 📊 Talk-To-Your-Database-AI

An interactive, production-ready web application that bridges the gap between non-technical business stakeholders and relational SQL databases using generative AI. Built with **Python, Streamlit, SQLite, and the Google Gemini API**.

---

## 🚀 Live Demo
🔗 **https://talk-to-your-database-ai.streamlit.app/**

---

## 💡 The Business Problem
In traditional data teams, up to **40% of an analyst's time** is spent writing ad-hoc `JOIN` and aggregation queries for managers. This creates operational bottlenecks and delays data-driven decision-making. 

This project solves that friction by allowing business managers to type questions in **plain English**, automatically converting them into secure, executable SQLite queries, and rendering instant dataframes and charts—reducing ad-hoc request turnaround time to seconds.

---

## 🛠️ Tech Stack & Architecture
* **Frontend & Deployment:** Streamlit / Streamlit Community Cloud
* **Backend & Logic:** Python, Pandas
* **Database Management:** SQLite (Multi-table relational schema with `customers`, `products`, and `orders`)
* **AI / LLM Integration:** Google GenAI SDK (`gemini-3.8-flash`) with prompt-engineered schema restriction
* **Reliability Engineering:** Built-in `@st.cache_data` response caching and zero-quota fallback handlers to ensure 100% uptime during high-traffic recruiter reviews.

---

## 🗄️ Database Schema
The app runs on a relational E-Commerce database structured with foreign-key relationships:
1. **`customers`** (`customer_id`, `name`, `region`)
2. **`products`** (`product_id`, `category`, `price`, `cost`)
3. **`orders`** (`order_id`, `customer_id`, `product_id`, `quantity`, `order_date`)

---

## 💻 Local Installation & Running Guide

If you want to run this project locally on your machine, follow these steps:

1. **Clone the repository:**
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name
2. **Install Dependencies**
   pip install -r requirements.txt
3. **Run the Streamlit app**
   streamlit run app.py

👨‍💻 Author
**Andrew Livingston V J**

B.Tech Computer Science & Engineering Graduate | Aspiring Data Analyst & Data Engineer

LinkedIn: https://www.linkedin.com/in/andrew-livingston-v-j-006987249/

GitHub: https://github.com/andrewlivingstonvj/
