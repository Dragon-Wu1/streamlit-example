import streamlit as st
from sqlalchemy import create_engine 
import pymysql

def connect():
   engine = create_engine('mysql+pymysql://username:password@host/dbname')  
   return engine

eng = connect()
con = eng.cursor()
query="SELECT * from instructors;"
con.execute(query)
st.write(con.fetchall())
