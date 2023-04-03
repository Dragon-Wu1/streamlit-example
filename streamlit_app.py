import streamlit as st


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

#conn = init_connection()

@st.cache(allow_output_mutation=True)
def get_connection():
    return create_engine("mssql+pyodbc://username:passowrd@DB_server/database?driver=ODBC+Driver+17+for+SQL+Server", 
    fast_executemany = True
    )
# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

#rows = run_query("SELECT * from mytable;")

# Print results.
#for row in rows:
    #st.write(f"{row[0]} has a :{row[1]}:")
st.write(get_connection())
