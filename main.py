import streamlit as st 
from auth import *

import streamlit as st
from auth import get_login_str

# Create a Streamlit login page
st.title("DZ Data Assistant")

# Sign In section
st.subheader("Sign In")

# Email input field
email = st.text_input("Email")

# Password input field
password = st.text_input("Password", type="password")

# Create columns for layout
col1, col2, col3 = st.columns([1, 6, 1])

# Divider (line between Sign In and Google Icon)
with col2:
    # Google Icon button with the Google logo
    google_button = get_login_str()
    st.markdown(google_button, unsafe_allow_html=True)
    

# Submit button
with col1:
    if st.button("Submit"):
        # Implement your authentication logic here using the 'email' and 'password' inputs
        if authenticate(email, password):
            # Successful login, redirect to your Streamlit app
            st.experimental_rerun()
            
            
