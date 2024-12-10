import streamlit as st
from utils import get_db_connection
import mysql.connector
from mysql.connector.errors import IntegrityError
import time
import random

def admin_control_page():
    # Check if the user is logged in as Admin
    if "logged_in" not in st.session_state or not st.session_state["logged_in"] or st.session_state.get("role") != "Admin":
        st.error("Unauthorized access. Please login as an Admin.")
        st.stop()

    # Create a container for the top row with right-aligned logout button
    col1, col2 = st.columns([4, 1])  # Create two columns, second one for the logout button

    with col1:
        st.title("Admin Control Panel")  # Title on the left

    with col2:
        # Add logout button on the right side, visible only for Admins
        if "role" in st.session_state and st.session_state["role"] == "Admin":
            if st.button("Logout"):
                # Clear session state for Admin
                st.session_state["logged_in"] = False
                st.session_state["role"] = None
                st.session_state["user"] = None
                st.success("You have logged out successfully!")
                time.sleep(1)
                st.rerun()  # Rerun to update the state

    # Database connection and cursor
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Tab layout for each table
    tabs = st.tabs(["Hotels", "Rooms", "Users", "Bookings"])

    # Hotels Table
    with tabs[0]:
        st.subheader("Hotels Management")
        cursor.execute("SELECT * FROM hotels")
        hotels = cursor.fetchall()
        st.dataframe(hotels, height=300)

        # Add a new hotel
        with st.expander("Add New Hotel"):
            hname = st.text_input("Hotel Name")
            haddress = st.text_input("Hotel Address")
            star = st.number_input("Star Rating", min_value=1, max_value=5, step=1)
            rating = st.number_input("Rating", min_value=0.0, max_value=5.0, step=0.1)
            if st.button("Add Hotel"):
                cursor.execute("INSERT INTO hotels (hname, haddress, star, rating) VALUES (%s, %s, %s, %s)", (hname, haddress, star, rating))
                conn.commit()
                st.success("Hotel added successfully!")
                time.sleep(1)
                st.rerun()

        # Modify a hotel
        with st.expander("Modify Hotel"):
            modify_hid = st.number_input("Enter Hotel ID to Modify", min_value=1, step=1)
            updated_hname = st.text_input("Updated Hotel Name")
            updated_haddress = st.text_input("Updated Hotel Address")
            updated_star = st.number_input("Updated Star Rating", min_value=1, max_value=5, step=1)
            updated_rating = st.number_input("Updated Rating", min_value=0.0, max_value=5.0, step=0.1)
            if st.button("Update Hotel"):
                cursor.execute(
                    "UPDATE hotels SET hname=%s, haddress=%s, star=%s, rating=%s WHERE hid=%s",
                    (updated_hname, updated_haddress, updated_star, updated_rating, modify_hid),
                )
                conn.commit()
                st.success("Hotel updated successfully!")
                time.sleep(1)
                st.rerun()

        # Delete a hotel
        with st.expander("Delete Hotel"):
            delete_hid = st.number_input("Enter Hotel ID to Delete", min_value=1, step=1)
            if st.button("Delete Hotel"):
                cursor.execute("DELETE FROM hotels WHERE hid = %s", (delete_hid,))
                conn.commit()
                st.success("Hotel deleted successfully!")
                time.sleep(1)
                st.rerun()

    # Rooms Table
    with tabs[1]:
        st.subheader("Rooms Management")
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        st.dataframe(rooms, height=300)

        # Add a new room
        with st.expander("Add New Room"):
            room_hid = st.number_input("Hotel ID", min_value=1, step=1, key="room_hid_add")
            rooms_count = st.number_input("Total Rooms", min_value=1, step=1, key="rooms_count_add")
            available_rooms = st.number_input("Available Rooms", min_value=0, max_value=rooms_count, step=1, key="available_rooms_add")
            price = st.number_input("Price per Room", min_value=0.0, step=0.1, key="price_add")

            # Check if the Hotel ID exists in the hotels table
            cursor.execute("SELECT * FROM hotels WHERE hid = %s", (room_hid,))
            hotel = cursor.fetchone()

            if hotel:
                if st.button("Add Room"):
                    cursor.execute(
                        "INSERT INTO rooms (hid, total_rooms, available, price_per_room) VALUES (%s, %s, %s, %s)",
                        (room_hid, rooms_count, available_rooms, price),
                    )
                    conn.commit()
                    st.success("Room added successfully!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error("The entered Hotel ID does not exist in the hotels table.")

        # Modify a room
        with st.expander("Modify Room"):
            modify_room_hid = st.number_input("Enter Hotel ID to Modify", min_value=1, step=1, key="modify_room_hid")
            updated_rooms = st.number_input("Updated Total Rooms", min_value=1, step=1, key="updated_rooms")
            updated_available_rooms = st.number_input("Updated Available Rooms", min_value=0, max_value=updated_rooms, step=1, key="updated_available_rooms")
            updated_price = st.number_input("Updated Price per Room", min_value=0.0, step=0.1, key="updated_price")

            # Check if the Hotel ID exists in the hotels table
            cursor.execute("SELECT * FROM hotels WHERE hid = %s", (modify_room_hid,))
            hotel = cursor.fetchone()

            if hotel:
                if st.button("Update Room"):
                    cursor.execute(
                        "UPDATE rooms SET total_rooms=%s, available=%s, price_per_room=%s WHERE hid=%s",
                        (updated_rooms, updated_available_rooms, updated_price, modify_room_hid),
                    )
                    conn.commit()
                    st.success("Room updated successfully!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error("The entered Hotel ID does not exist in the hotels table.")

        # Delete a room
        with st.expander("Delete Room"):
            delete_room_hid = st.number_input("Enter Hotel ID to Delete Rooms", min_value=1000, max_value=9999, step=1)
            if st.button("Delete Room"):
                # Check if the entered Hotel ID exists in the hotels table
                cursor.execute("SELECT * FROM hotels WHERE hid = %s", (delete_room_hid,))
                hotel = cursor.fetchone()

                if hotel:  # If the hotel exists
                    cursor.execute("DELETE FROM rooms WHERE hid = %s", (delete_room_hid,))
                    conn.commit()
                    st.success("Room deleted successfully!")
                else:
                    st.warning("Hotel with the entered ID does not exist.")
                time.sleep(3)
                st.rerun()

    # Users Table
    with tabs[2]:
        st.subheader("Users Management")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        st.dataframe(users, height=300)

        # Add a new user
        with st.expander("Add New User"):
            name = st.text_input("Name")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            phone = st.text_input("Phone")
            address = st.text_input("Address")
            email = st.text_input("Email")

            if st.button("Add User"):
                try:
                    random_uid = random.randint(1000, 9999)

                    cursor.execute(
                        "INSERT INTO users (uid, name, username, password, phone, address, email) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (random_uid, name, username, password, phone, address, email),
                    )
                    conn.commit()
                    st.success("User added successfully!")
                    time.sleep(1)
                    st.rerun()
                except IntegrityError as e:
                    if e.errno == 1062:  # Duplicate entry error code
                        st.warning(f"Username '{username}' already exists. Please choose a different username.")
                    else:
                        st.error(f"An unexpected error occurred: {e}")

        # Delete a user
        with st.expander("Delete User"):
            delete_uid = st.number_input("Enter User ID to Delete", min_value=1000, max_value=9999, step=1)
            if st.button("Delete User"):
                # Check if the entered User ID exists in the users table
                cursor.execute("SELECT * FROM users WHERE uid = %s", (delete_uid,))
                user = cursor.fetchone()

                if user:  # If the user exists
                    cursor.execute("DELETE FROM users WHERE uid = %s", (delete_uid,))
                    conn.commit()
                    st.success("User deleted successfully!")
                else:
                    st.warning("User with the entered ID does not exist.")
                time.sleep(3)  
                st.rerun() 

    # Bookings Table
    with tabs[3]:
        st.subheader("Bookings Management")
        cursor.execute("SELECT * FROM bookings")
        bookings = cursor.fetchall()
        st.dataframe(bookings, height=300)

        # Add a new booking
        with st.expander("Add New Booking"):
            user_id = st.number_input("User ID", min_value=1000, max_value=9999, step=1)
            hotel_id = st.number_input("Hotel ID", min_value=1000, max_value=9999, step=1)
            room_count = st.number_input("Room Count", min_value=1, step=1)
            amount_paid = st.number_input("Amount Paid", min_value=0.0, step=0.1)
            check_in_date = st.date_input("Check-In Date")
            check_out_date = st.date_input("Check-Out Date")
            
            if st.button("Add Booking"):
                # Check if the user exists in the 'users' table
                cursor.execute("SELECT * FROM users WHERE uid = %s", (user_id,))
                user = cursor.fetchone()

                if user:  # If the user exists
                    cursor.execute(
                        "INSERT INTO bookings (user_id, hotel_id, room_count, amount_paid, check_in_date, check_out_date) VALUES (%s, %s, %s, %s, %s, %s)",
                        (user_id, hotel_id, room_count, amount_paid, check_in_date, check_out_date)
                    )
                    conn.commit()
                    st.success("Booking added successfully!")
                    time.sleep(1)
                    st.rerun()
                else:  # If the user does not exist
                    st.warning("User not exists. First, add user into the database.")

        # Delete a booking
        with st.expander("Delete Booking"):
            delete_booking_id = st.number_input("Enter Booking ID to Delete", min_value=1, step=1)
            if st.button("Delete Booking"):
                # Check if the entered Booking ID exists in the bookings table
                cursor.execute("SELECT * FROM bookings WHERE booking_id = %s", (delete_booking_id,))
                booking = cursor.fetchone()

                if booking:  # If the booking exists
                    cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (delete_booking_id,))
                    conn.commit()
                    st.success("Booking deleted successfully!")
                else:
                    st.warning("Booking with the entered ID does not exist.")
                time.sleep(3)
                st.rerun()

    # Close database connection and cursor
    cursor.close()
    conn.close()
