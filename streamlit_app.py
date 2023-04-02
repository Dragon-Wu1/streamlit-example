# streamlit_app.py

import streamlit as st
import mysql.connector

# Initialize connection.
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()
cursor = conn.cursor()
sql="SELECT * from instructors;"
cursor.execute(sql)
df = cursor.fetchall()
st.write(df)

