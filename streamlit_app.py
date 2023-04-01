import time
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import smtplib
import email.message
#import pymysql
import mysql.connector

def send_email(*email_list):
    for i in email_list:
        msg = email.message.EmailMessage()
        sender_email = "dragonhunter9527@gmail.com"
        receiver_email = i  # dragonwu9523@gmail.com
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Course information"
        msg.add_alternative(
            "<h3>The link for filled the information of course</h3><h4>The link below</h4></br>http://192.168.31.97:8501",
            subtype="html")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("dragonhunter9527@gmail.com", "xvkhdwolxkdsocif")
        server.send_message(msg)
        server.close()


def query(cursor):
    sql = 'Select course_id,course_name , status, email from course M Join instructors F On M.course_name = F.course;'
    cursor.execute(sql)
    db.commit()
    df2 = pd.read_sql(sql, con=db)
    return df2


def user_login(cursor, name, password):
    bo = 1
    sql = "Select password from instructors Where name = '%s';" % (name)
    cursor.execute(sql)
    db.commit()
    df2 = cursor.fetchone()
    if df2 is not None and df2[0] == password:
        pass
    else:
        bo = 0
    return bo


def inputdata(cursor, des, pre, tex, ref, maj, obj, cov, obo, csn):
    sql = "UPDATE course SET description = '%s', prerequisites = '%s', textbook = '%s', reference = '%s', major_pre = " \
          "'%s', objectives = '%s', covered = '%s', objectives_outcomes = '%s' WHERE course_name = '%s'" % (des,
                                                                                                            pre,
                                                                                                            tex,
                                                                                                            ref, maj,
                                                                                                            obj, cov,
                                                                                                            obo, csn)
    cursor.execute(sql)
    db.commit()


def main():
    ver = 0
    st.title('FST')
    image = Image.open('UM_logo.jpg')
    st.image(image)
    menu = ["Sign up", "Course", "Admin"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Sign up":
        st.subheader("Sign up")
        with st.form(key='form1'):
            user = st.text_input("User Name")
            password = st.text_input("Password")
            email = st.text_input("Email address")
            submit_button = st.form_submit_button(label='Sign in')
        if submit_button:
            ver = user_login(cursor, user, password)
            if bool(ver):
                st.success("You have successfully sign in!")
            else:
                st.write("The password or account is not correct")
                #st.stop()    #be marked
                #st.success("The password or account is not correct")

    else: #choice == "Course" and bool(ver):
        st.subheader("Course Form")
        with st.form(key='form2'):
            course_code = st.text_input("Course Code")
            catalog_description = st.text_input("Catalog Description")
            prerequisites = st.text_input("Prerequisites")
            Textbook = st.text_input("Textbook(s) and other required materia")
            References = st.text_input("References")
            Major_prerequisites_by_topic = st.text_input("Major prerequisites by topic")
            Course_objectives = st.text_input("Course objectives")
            Topics_covered = st.text_input("Topics covered")
            objectives_and_outcomes = st.text_input("Relationship to CEE, EEE and EME program objectives and outcomes")
            submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            inputdata(cursor, catalog_description, prerequisites, Textbook, References, Major_prerequisites_by_topic, Course_objectives, Topics_covered, objectives_and_outcomes, course_code)
            st.success("You have successfully submitted!")

    if choice == "Admin":
        st.subheader("Admin")
        button_list = []
        email_list = []
        with st.form(key='form3'):
            df2 = query(cursor)
            #for row in df2:
            #course_id = df2[["course_id"]]
            course_name = df2[["course_name"]]
            #status = df2[["status"]]
            #email_n = df2[["email"]]
            left_column, right_column = st.columns([3, 1])
            with left_column:
                st.write(df2)

            with right_column:
                select_all = st.checkbox("All")
                for j in df2.course_name:
                    j = st.checkbox(j)
                    button_list.append(j)

                #st.write(type(button_list))
                #st.write(button_list[0])
            submit_button = st.form_submit_button(label='Select Finish')
            if submit_button:
                #st.write(button_list)
                for t in range(0, len(button_list)):
                    if button_list[t]:
                        #email_list.append(email_n[t])
                        email_list.append(df2.at[t, "email"])

                st.write(email_list)
                send_email(email_list)
                st.success("You have successfully send email!")


if __name__ == '__main__':
    db = mysql.connector.connect(**st.secrets["mysql"])    
    cursor = db.cursor()
    main()
    #st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
    #    .mark_circle(color='#0068c9', opacity=0.5)
    #    .encode(x='x:Q', y='y:Q'))
