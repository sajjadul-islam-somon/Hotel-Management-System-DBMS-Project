import streamlit as st
from utils import get_db_connection

def home_page():
    # Ensure the user is logged in and session state for "user" is available
    if "user" not in st.session_state or st.session_state["user"] is None or "uid" not in st.session_state["user"]:
        st.error("Please login first.")
        st.stop()

    # Header layout with a Logout button in the first row, right-aligned
    header_col1, header_col2 = st.columns([4, 1])
    with header_col1:
        st.title("Hotel Booking System")
    with header_col2:
        # Check if the logged-in user is a "User" and show the logout button only for them
        if "role" in st.session_state and st.session_state["role"] == "User":
            if st.button("Logout"):
                st.session_state.clear()  # Clear session state for the user
                st.success("You have been logged out.")
                st.rerun()  # Redirect to Login Page

    # Subheader showing the logged-in user's name
    st.subheader(f"Welcome, {st.session_state['user']['name']}!")

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Display hotels table
    st.subheader("Hotels")
    cursor.execute("SELECT hid AS ID, hname AS Name, haddress AS Location, star as Star, rating as Rating FROM hotels")
    hotels = cursor.fetchall()
    st.dataframe(hotels, height=300)  # Set height for scrollbar

    # Create three buttons side by side: "Price-Wise Hotels", "Most Popular Hotels", and "Your Booked Rooms"
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        show_price_wise = st.button("Price-Wise Hotels")
    with col2:
        show_popular_hotels = st.button("Most Popular Hotels")
    with col3:
        show_booked_rooms = st.button("Your Booked Rooms")

    # Show Price-Wise Hotels if the button is clicked
    if show_price_wise:
        st.subheader("Price-Wise Hotels")
        query = """
        SELECT hotels.hid AS ID, hotels.hname AS Name, hotels.haddress AS Location, rooms.price_per_room AS 'Per Room Price'
        FROM rooms
        JOIN hotels ON rooms.hid = hotels.hid
        ORDER BY rooms.price_per_room ASC
        """

        cursor.execute(query)
        price_wise_hotels = cursor.fetchall()
        st.dataframe(price_wise_hotels, height=300)  # Set height for scrollbar

    # Show Most Popular Hotels if the button is clicked
    if show_popular_hotels:
        st.subheader("Most Popular Hotels")
        query = """
            SELECT hotels.hid AS ID, hotels.hname AS Name, rooms.price_per_room AS 'Per Room Price', hotels.star AS Star, hotels.rating AS Rating
            FROM hotels
            JOIN rooms ON hotels.hid = rooms.hid
            ORDER BY hotels.rating DESC
        """

        cursor.execute(query)
        most_popular_hotels = cursor.fetchall()
        st.dataframe(most_popular_hotels, height=300)  # Set height for scrollbar

    # Show Your Booked Rooms if the button is clicked
    if show_booked_rooms:
        st.subheader("Your Booked Rooms")

        # Fetching the logged-in user's ID from session state
        user_id = st.session_state["user"]["uid"]  # Corrected to use 'uid'
        
        query = """
            SELECT  b.booking_id AS 'Booking ID', 
                    u.name AS 'User Name', 
                    h.hname AS 'Hotel Name', 
                    b.room_count AS 'Rooms Booked', 
                    b.amount_paid AS 'Amount Paid', 
                    b.check_in_date AS 'Check-In Date', 
                    b.check_out_date AS 'Check-Out Date'
            FROM bookings b
            JOIN hotels h ON b.hotel_id = h.hid
            JOIN users u ON b.user_id = u.uid
            WHERE b.user_id = %s
            """

        cursor.execute(query, (user_id,))
        booked_rooms = cursor.fetchall()

        if booked_rooms:
            st.table(booked_rooms)  # Display results in a table
        else:
            st.write("You have no booked rooms.")
        
        cursor.close()
        conn.close()
