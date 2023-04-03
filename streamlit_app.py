import streamlit as st
from sqlalchemy import create_engine 
import pymysql


engine = create_engine('mysql+pymysql://username:password@host/dbname')  
con = engine.cursor()
query="SELECT * from instructors;"
con.execute(query)
st.write(con.fetchall())
