import streamlit as st
import snowflake.connector
from PIL import Image

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()


def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )


def inputdata(des, pre, tex, ref, maj, obj, cov, obo, csn):
    conn = init_connection()
    cursor = conn.cursor()
    sql = "UPDATE course SET description = '%s', prerequisites = '%s', textbook = '%s', reference = '%s', major_pre = " \
          "'%s', objectives = '%s', covered = '%s', objectives_outcomes = '%s' WHERE course_name = '%s'" % (des,
                                                                                                            pre,
                                                                                                            tex,
                                                                                                            ref, maj,
                                                                                                            obj, cov,
                                                                                                            obo, csn)
    cursor.execute(sql)
    conn.commit()
    st.write("input successfully")


def show_main_page():
    with mainSection:
        st.title('FST')
        image = Image.open('UM_logo.jpg')
        st.image(image)
        course_code = st.text_input("Course Code")
        catalog_description = st.text_input("Catalog Description")
        prerequisites = st.text_input("Prerequisites")
        Textbook = st.text_input("Textbook(s) and other required materia")
        References = st.text_input("References")
        Major_prerequisites_by_topic = st.text_input("Major prerequisites by topic")
        Course_objectives = st.text_input("Course objectives")
        Topics_covered = st.text_input("Topics covered")
        objectives_and_outcomes = st.text_input("Relationship to CEE, EEE and EME program objectives and outcomes")
        Sub_Mit = st.button("Submit Input")
        if Sub_Mit:
            inputdata(catalog_description, prerequisites, Textbook, References, Major_prerequisites_by_topic, Course_objectives, Topics_covered, objectives_and_outcomes, course_code)


def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False


def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)


def LoggedIn_Clicked(userName, password):
    conn = init_connection()
    cursor = conn.cursor()
    sql = "Select password from instructors Where name = '%s';" % (userName)
    cursor.execute(sql)
    conn.commit()
    df2 = cursor.fetchone()
    if df2 is not None and df2[0] == password:
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")


def show_login_page():
    with loginSection:
        if st.session_state['loggedIn'] == False:
            userName = st.text_input(label="", value="", placeholder="Enter your user name")
            password = st.text_input(label="", value="", placeholder="Enter password", type="password")
            st.button("Login", on_click=LoggedIn_Clicked, args=(userName, password))


with headerSection:
    st.title("User")
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        if st.session_state['loggedIn']:
            show_logout_page()
            show_main_page()
        else:
            show_login_page()

