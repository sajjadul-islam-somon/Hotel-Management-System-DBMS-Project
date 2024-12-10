import streamlit as st
from utils import get_db_connection
import time

def signup_page():
    st.title("Signup Page")

    name = st.text_input("Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    phone = st.text_input("Phone")
    address = st.text_input("Address")
    email = st.text_input("Email")
    confirmation = st.checkbox("I confirm the details are correct")

    if st.button("Sign Up"):
        if not (name and username and password and phone and address and email):
            st.error("All fields must be filled!")
        elif not confirmation:
            st.error("Please confirm the details to proceed.")
        else:
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "INSERT INTO users (name, username, password, phone, address, email) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, username, password, phone, address, email),
                )
                conn.commit()
                st.success("Signup successful! Redirecting to login page...")
                time.sleep(2)
                st.rerun()  # Use st.rerun to reload the page or redirect
            except Exception as e:
                st.error(f"Error during signup: {e}")
            finally:
                cursor.close()
                conn.close()
