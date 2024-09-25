import streamlit as st

with st.form(key='signup_form'):
    st.title('Sign up')
    
    username = st.text_input('Enter username')
    password = st.text_input('Password', type='password') 
    mobile = st.text_input('Enter mobile no.')
    city = st.text_input('Enter City')
    
    submit = st.form_submit_button("Submit")

# Handle form submission
if submit:
    st.success(f"User {username} signed up successfully!")

