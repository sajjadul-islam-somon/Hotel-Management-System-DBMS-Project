import streamlit as st
from login import login_page
from signup import signup_page
from home import home_page
from admin_control import admin_control_page
from book_now import book_now_page

# Add sidebar menu
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Login", "Signup", "Home", "Book Now", "Admin Control"])

# Routing logic based on the page selected from the sidebar
if page == "Login":
    login_page()
elif page == "Signup":
    signup_page()
elif page == "Home":
    home_page() 
elif page == "Book Now":
    book_now_page() 
elif page == "Admin Control":
    admin_control_page()
