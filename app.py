import streamlit as st
import os
from login import login_page
from signup import signup_page
from home import home_page
from admin_control import admin_control_page
from book_now import book_now_page


# Sidebar Navigation
st.sidebar.image("EasyBook.png", use_container_width=True)
st.sidebar.markdown("<h2 style='text-align: center;'>EasyBook</h2>", unsafe_allow_html=True)

# Define navigation options with images
navigation_options = {
    "Login": "Login.png",
    "Signup": "Signup.png",
    "Home": "Home.png",
    "Book Now": "BookNow.png",
    "Admin Control": "AdminControl.png"
}

# Use session state to track the selected page
if "selected_page" not in st.session_state:
    st.session_state.selected_page = None

# Create clickable buttons
for page_name, img_path in navigation_options.items():
    if st.sidebar.button(label=f"{page_name}", key=page_name):
        st.session_state.selected_page = page_name

# Display the corresponding page content based on the selected page
if st.session_state.selected_page == "Login":
    login_page()
elif st.session_state.selected_page == "Signup":
    signup_page()
elif st.session_state.selected_page == "Home":
    home_page()
elif st.session_state.selected_page == "Book Now":
    book_now_page()
elif st.session_state.selected_page == "Admin Control":
    admin_control_page()
else:
    st.markdown(
    """<div style='text-align: center;'>
    <h1>Welcome to EasyBook</h1>
    </div>""",
    unsafe_allow_html=True
    )
    # Load and play the video
    try:
        st.video("welcome_video.mp4", start_time=0)
    except Exception as e:
        st.error(f"Error loading video: {e}")
