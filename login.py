import streamlit as st
from utils import get_db_connection

def login_page():
    st.title("Login")

    # Login form
    role = st.selectbox("Select Role", ["User", "Admin"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Check if switching between User and Admin roles
        if "role" in st.session_state:
            if st.session_state["role"] != role:
                # If switching roles, clear the previous session
                st.session_state.clear()
                st.success(f"{st.session_state.get('role', 'Previous session')} logged out automatically.")
        
        # Admin login
        if role == "Admin":
            # Hardcoded admin credentials
            admin_username = "admin"
            admin_password = "admin"

            if username == admin_username and password == admin_password:
                st.success("Welcome, Admin!")
                st.session_state["logged_in"] = True
                st.session_state["role"] = "Admin"
                st.session_state["current_page"] = "AdminControl"  # Set current page
            else:
                st.error("Invalid Admin credentials")
        
        # User login
        else:
            # User login validation from the database
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                st.success(f"Welcome, {user['name']}!")
                st.session_state["logged_in"] = True
                st.session_state["role"] = "User"
                st.session_state["user"] = user
                st.session_state["current_page"] = "Home"  # Set current page
            else:
                st.error("Invalid User credentials")

            cursor.close()
            conn.close()
