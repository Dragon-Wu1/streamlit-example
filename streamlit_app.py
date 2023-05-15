import streamlit as st
import snowflake.connector
from PIL import Image
import time
import pandas as pd
import time

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()
FillSection = st.container()
DataSection = st.container()

st.markdown(
    """<style>
        button {
            height: 1em;     
        }
        </style>""",
    unsafe_allow_html=True,
)

def data_click():
    st.session_state['Fill'] = True
    st.session_state['Data'] = False
    
    
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )


def show_input_page():
    with DataSection:
        if st.session_state['Data']:
            st.markdown(f"\n"
                        f"            Information：\n"
                        f"            - Name : {st.session_state['csn']}\n"
                        f"            - Description : {st.session_state['des']}\n"
                        f"            - Prerequisites : {st.session_state['pre']}\n"
                        f"            - Textbook : {st.session_state['tex']}\n"
                        f"            - Reference : {st.session_state['ref']}\n"
                        f"            - Major : {st.session_state['maj']}\n"
                        f"            - Objectives : {st.session_state['obj']}\n"
                        f"            - Covered : {st.session_state['cov']}\n"
                        f"            - Objectives Outcomes : {st.session_state['obo']}\n"
                        f"            ")
            conn = init_connection()
            cursor = conn.cursor()
            sql = "UPDATE course SET description = '%s', prerequisites = '%s', textbook = '%s', reference = '%s', " \
              "major_pre = " \
              "'%s', objectives = '%s', covered = '%s', objectives_outcomes = '%s' WHERE id_name = '%s'" % (st.session_state['des'],
                                                                                                            st.session_state['pre'],
                                                                                                            st.session_state['tex'],
                                                                                                            st.session_state['ref'], st.session_state['maj'],
                                                                                                            st.session_state['obj'], st.session_state['cov'],
                                                                                                            st.session_state['obo'], st.session_state['csn'])
            cursor.execute(sql)
            conn.commit()
            left_column, right_column, outcol= st.columns([3, 1, 1])
            with left_column:
                back_save = st.button("Back", key='back_save', on_click=data_click)
            with right_column:
                confirm = st.button('Confirm')
            with outcol:
                st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)
            if confirm:
                sql1 = "UPDATE course SET status = 'Finished' WHERE id_name = '%s'" % (st.session_state['csn'])
                cursor.execute(sql1)
                conn.commit()
                st.success("Modifying is successfully")



def read():
    name = st.session_state['UserName']
    conn = init_connection()
    cursor = conn.cursor()
    sql = "Select id_name as Course_Code, course_name as Course_Name, course_dept as Course_Department, status as " \
          "Course_Status from course M Join instructors F On M.id_name = F.course " \
          "AND F.name = '%s'" % (
              name)
    cursor.execute(sql)
    conn.commit()
    df2 = pd.read_sql(sql, con=conn)  # it read the result as a dataframe very important
    return df2


def convert_tuple(tup):  # convert tuple to string
    str = ''.join(tup)
    return str


def loading(code):
    conn = init_connection()
    cursor = conn.cursor()
    sql = "Select * from course Where id_name = '%s'" % (
        code)
    cursor.execute(sql)
    conn.commit()
    df2 = cursor.fetchall()
    #df2 = pd.read_sql(sql, con=db)  #it read the result as a dataframe very important
    return df2


def convertTuple(tup):      #convert tuple to string
    str = ''.join(tup)
    return str


def show_login_page():
    with loginSection:
        st.title("User")
        if st.session_state['loggedIn'] == False:
            userName = st.text_input(label="", value="", placeholder="Enter your user name")
            password = st.text_input(label="", value="", placeholder="Enter password", type="password")
            st.button("Login", on_click=LoggedIn_Clicked, args=(userName, password))
            
            
def LoggedIn_Clicked(userName, password):
    conn = init_connection()
    cursor = conn.cursor()
    sql = "Select * from instructors Where name = '%s';" % (userName)
    cursor.execute(sql)
    conn.commit()
    df2 = cursor.fetchone()

    #st.write(df2[3])
    #st.write(type(df2[3]))
    st.write(password)
    st.write(type(password))
    df = str(df2[3])
    #password = int(password) #as password is a string and df2 is tuple
    if df2 is not None and df == password:
        st.session_state['loggedIn'] = True
        if 'User' not in st.session_state:
            st.session_state['UserName'] = userName
        if 'Password' not in st.session_state:
            st.session_state['Password'] = df
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")


def LoggedOut_Clicked():
    #st.session_state['loggedIn'] = False
    for key in st.session_state.keys():
        del st.session_state[key]

def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)


def main_click(*cour):
    st.session_state['main'] = False
    st.session_state['Fill'] = True
    if 'name' not in st.session_state:
        st.session_state['name'] = convert_tuple(cour)  # the paramater of course code and cour is a tuple
    else:
        st.session_state['name'] = convert_tuple(cour)
        
        
def fill_click1(*ll):
    st.session_state['Fill'] = False
    st.session_state['Data'] = True
    if 'des' not in st.session_state:
        st.session_state['des'] = ll[0]
    else:
        st.session_state['des'] = ll[0]
    if 'pre' not in st.session_state:
        st.session_state['pre'] = ll[1]
    else:
        st.session_state['pre'] = ll[1]
    if 'tex' not in st.session_state:
        st.session_state['tex'] = ll[2]
    else:
        st.session_state['tex'] = ll[2]
    if 'ref' not in st.session_state:
        st.session_state['ref'] = ll[3]
    else:
        st.session_state['ref'] = ll[3]
    if 'maj' not in st.session_state:
        st.session_state['maj'] = ll[4]
    else:
        st.session_state['maj'] = ll[4]
    if 'obj' not in st.session_state:
        st.session_state['obj'] = ll[5]
    else:
        st.session_state['obj'] = ll[5]
    if 'cov' not in st.session_state:
        st.session_state['cov'] = ll[6]
    else:
        st.session_state['cov'] = ll[6]
    if 'obo' not in st.session_state:
        st.session_state['obo'] = ll[7]
    else:
        st.session_state['obo'] = ll[7]
    if 'csn' not in st.session_state:
        st.session_state['csn'] = ll[8]
    else:
        st.session_state['csn'] = ll[8]

def fill_click2():
    st.session_state['Fill'] = False
    st.session_state['main'] = True
    
def show_fill_page():
    if st.session_state['main'] == False and st.session_state['Fill'] == True:
        with FillSection:
            st.title('Filled the information in below.')
            course_code = st.session_state['name']
            df = loading(course_code)
            df1 = df[0]
            if df1[4] != None:
                catalog_description = st.text_area("Catalog Description", df1[4])
            else:
                catalog_description = st.text_area("Catalog Description")

            if df1[5] != None:
                prerequisites = st.text_area("Prerequisites", df1[5])
            else:
                prerequisites = st.text_area("Prerequisites")

            if df1[6] != None:
                textbook = st.text_area("Textbook(s) and other required materia", df1[6])
            else:
                textbook = st.text_area("Textbook(s) and other required materia")

            if df1[7] != None:
                references = st.text_area("References", df1[7])
            else:
                references = st.text_area("References")

            if df1[8] != None:
                major_prerequisites_by_topic = st.text_area("Major prerequisites by topic", df1[8])
            else:
                major_prerequisites_by_topic = st.text_area("Major prerequisites by topic")

            if df1[9] != None:
                course_objectives = st.text_area("Course objectives", df1[9])
            else:
                course_objectives = st.text_area("Course objectives")

            if df1[10] != None:
                topics_covered = st.text_area("Topics covered", df1[10])
            else:
                topics_covered = st.text_area("Topics covered")

            if df1[11] != None:
                objectives_and_outcomes = st.text_area(
                    "Relationship to CEE, EEE and EME program objectives and outcomes", df1[11])
            else:
                objectives_and_outcomes = st.text_area(
                    "Relationship to CEE, EEE and EME program objectives and outcomes")
            left_column, right_column, outcol1 = st.columns([3, 1, 1])
            with left_column:
                back = st.button("Back", on_click=fill_click2)
            with right_column:
                list123 = [catalog_description, prerequisites, textbook, references, major_prerequisites_by_topic, course_objectives, topics_covered, objectives_and_outcomes, course_code]
                sub_mit = st.button("Save", on_click=fill_click1, args=list123)
            with outcol1:
                st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)


def show_main_page():
    if st.session_state['main']:
        with mainSection:
            st.title('WELCOME TO ' + st.session_state['UserName'] + '!')
            df2 = read()  # return is tuples
            st.table(df2)
            select_course = st.selectbox('Select the course to modify', df2.Course_Code)
            i = st.button('Modify', key='i', on_click=main_click, args=select_course)


with headerSection:
    conn = init_connection()
    cursor = conn.cursor()
    #st.write(1)
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        # st.write(2)
        if st.session_state['loggedIn']:
            if 'main' not in st.session_state:
                st.session_state['main'] = True
                if 'Fill' not in st.session_state:
                    st.session_state['Fill'] = False
                if 'Data' not in st.session_state:
                    st.session_state['Data'] = False
                # st.write(3)
                show_main_page()  # main false,fill true
            else:
                # st.write(4)
                show_main_page()
                # st.write(5)
                show_fill_page()
                show_input_page()
        else:
            show_login_page()
