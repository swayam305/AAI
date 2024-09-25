import streamlit as st
from datetime import datetime
import json
import os
import pandas as pd
import plotly.express as px
 
# JSON file to store user data
USER_DB = 'users.json'
 
# Function to load user data from the JSON file
def load_user_data():
    if os.path.exists(USER_DB):
        with open(USER_DB, 'r') as file:
            return json.load(file)
    else:
        return {}
 
# Function to save user data to the JSON file
def save_user_data(user_data):
    with open(USER_DB, 'w') as file:
        json.dump(user_data, file, indent=4)
 
# Function to save marks in a user-specific CSV file
def save_marks(email, marks):
    file_name = f"{email}_marks.csv"
    subjects = ['Math', 'Science', 'English', 'History', 'Geography', 'Computer Science', 'Physical Education']
    marks_data = pd.DataFrame({"Subject": subjects, "Marks": marks})
    marks_data.to_csv(file_name, index=False)
    st.success(f"Marks saved to {file_name}!")
 
# Function to load marks from user-specific CSV file
def load_marks(email):
    file_name = f"{email}_marks.csv"
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        st.error("No marks found. Please enter marks first.")
        return None
 
# Function to handle signup
def sign_up():
    st.header("Sign Up")
 
    with st.form(key="signup_form"):
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        dob = st.date_input("Date of Birth", value=datetime(2000, 1, 1))
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
 
        submit_button = st.form_submit_button(label="Sign Up")
 
        if submit_button:
            user_data = load_user_data()
 
            if email in user_data:
                st.error("This email is already registered!")
            else:
                user_data[email] = {"name": name, "phone": phone, "dob": str(dob), "password": password}
                save_user_data(user_data)
                st.success(f"Account created for {name}!")
 
# Function to handle login
def login():
    st.header("Login")
 
    with st.form(key="login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
       
        submit_button = st.form_submit_button(label="Login")
       
        if submit_button:
            user_data = load_user_data()
 
            if email not in user_data:
                st.error("Email not found. Please sign up first!")
            elif user_data[email]["password"] != password:
                st.error("Incorrect password. Try again!")
            else:
                st.success(f"Welcome back, {user_data[email]['name']}!")
                st.session_state['logged_in'] = True
                st.session_state['email'] = email
                st.rerun()
 
# Page to enter marks using sliders
def input_marks():
    st.header("Enter Marks for 7 Subjects")
 
    math_marks = st.slider("Math", 0, 100, 50)
    science_marks = st.slider("Science", 0, 100, 50)
    english_marks = st.slider("English", 0, 100, 50)
    history_marks = st.slider("History", 0, 100, 50)
    geography_marks = st.slider("Geography", 0, 100, 50)
    cs_marks = st.slider("Computer Science", 0, 100, 50)
    pe_marks = st.slider("Physical Education", 0, 100, 50)
 
    marks = [math_marks, science_marks, english_marks, history_marks, geography_marks, cs_marks, pe_marks]
   
    if st.button("Submit Marks"):
        save_marks(st.session_state['email'], marks)
 
# Function to display graphs using plotly
def display_graphs():
    st.header("Your Marks")
 
    marks_data = load_marks(st.session_state['email'])
 
    if marks_data is not None:
        st.write("Here are your Reports:")
 
        # Bar chart
        fig = px.bar(marks_data, x='Subject', y='Marks', title="Marks per Subject")
        st.plotly_chart(fig)
 
        # Line chart
        fig_line = px.line(marks_data, x='Subject', y='Marks', title="Marks Trend")
        st.plotly_chart(fig_line)
 
# Main app layout with sidebar navigation
def main():
    st.sidebar.title("Navigation")
   
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
   
    if st.session_state['logged_in']:
        choice = st.sidebar.selectbox("Choose Action", ["Enter Marks", "View Graphs", "Logout"])
       
        if choice == "Enter Marks":
            input_marks()
        elif choice == "View Graphs":
            display_graphs()
        elif choice == "Logout":
            st.session_state['logged_in'] = False
            st.session_state['email'] = None
            st.sidebar.success("Logged out successfully.")
            st.rerun()
    else:
        choice = st.sidebar.selectbox("Choose Action", ["Sign Up", "Login"])
 
        if choice == "Sign Up":
            sign_up()
        elif choice == "Login":
            login()
 
if __name__ == '__main__':
    main()