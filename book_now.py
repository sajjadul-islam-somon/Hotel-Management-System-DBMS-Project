import streamlit as st
from utils import get_db_connection
import datetime

def book_now_page():
    # Title for the Book Now page
    st.title("Book a Hotel")

    # Check if the user is logged in
    if "user" not in st.session_state or st.session_state["user"] is None or "uid" not in st.session_state["user"]:
        st.error("You must be logged in to book a hotel.")
        return  # Stop further execution if the user is not logged in

    user_id = st.session_state["user"]["uid"]

    # Tab layout for each Booking style
    tabs = st.tabs(["By Hotel's Name", "By Price & Room Needed"])

    # Book by Hotel Name Tab
    with tabs[0]:
        st.subheader("Search Hotels by Name")
        search_query = st.text_input("Enter hotel name to search:")

        if search_query:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            try:
                # Search hotels by name
                query = """
                    SELECT hotels.hid AS ID, hotels.hname AS Name, rooms.available AS 'Available Rooms', 
                           rooms.price_per_room AS 'Per Room Price'
                    FROM rooms
                    JOIN hotels ON rooms.hid = hotels.hid
                    WHERE hotels.hname LIKE %s
                    ORDER BY rooms.price_per_room ASC
                """
                cursor.execute(query, ('%' + search_query + '%',))
                results = cursor.fetchall()

                if results:
                    hotel_names = [
                        f"{row['Name']} - {row['Available Rooms']} rooms available - ${row['Per Room Price']}" 
                        for row in results
                    ]
                    selected_hotel = st.radio("Select a Hotel to Book:", hotel_names)
                    selected_hotel_details = next(
                        (hotel for hotel in results if f"{hotel['Name']} - {hotel['Available Rooms']} rooms available - ${hotel['Per Room Price']}" == selected_hotel),
                        None
                    )

                    if selected_hotel_details:
                        st.write(f"**Hotel Name**: {selected_hotel_details['Name']}")
                        num_rooms = st.number_input(
                            "Enter number of Rooms:", 
                            min_value=1, 
                            max_value=selected_hotel_details['Available Rooms'], 
                            step=1
                        )

                        if num_rooms > 0:
                            total_price = num_rooms * selected_hotel_details['Per Room Price']
                            st.write(f"Total Price: ${total_price}")

                            if st.button("Proceed to Book", key="book_by_name"):
                                try:
                                    # Update rooms and insert booking
                                    update_rooms_query = """
                                        UPDATE rooms
                                        SET available = available - %s
                                        WHERE hid = %s
                                    """
                                    cursor.execute(update_rooms_query, (num_rooms, selected_hotel_details['ID']))

                                    insert_booking_query = """
                                        INSERT INTO bookings (user_id, hotel_id, room_count, amount_paid, check_in_date, check_out_date)
                                        VALUES (%s, %s, %s, %s, %s, %s)
                                    """
                                    check_in_date = datetime.date.today()
                                    check_out_date = check_in_date + datetime.timedelta(days=2)
                                    cursor.execute(insert_booking_query, (user_id, selected_hotel_details['ID'], num_rooms, total_price, check_in_date, check_out_date))

                                    conn.commit()
                                    st.success(f"You've booked {num_rooms} rooms at {selected_hotel_details['Name']}! Total: ${total_price}. Proceed with payment.")
                                except Exception as e:
                                    st.error(f"Booking failed: {e}")
                else:
                    st.write("No matching hotels found.")
            finally:
                cursor.close()
                conn.close()

    # Book by Price and Rooms Tab
    with tabs[1]:
        st.subheader("Search Hotels by Price and Available Rooms")
        max_price = st.number_input("Enter maximum price per room ($)", min_value=1, step=1)
        num_rooms_needed = st.number_input("Number of Room Needs (Rooms to Book)", min_value=1, step=1)

        if max_price and num_rooms_needed:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            try:
                query = """
                    SELECT hotels.hid AS ID, hotels.hname AS Name, rooms.available AS 'Available Rooms', 
                           rooms.price_per_room AS 'Per Room Price'
                    FROM rooms
                    JOIN hotels ON rooms.hid = hotels.hid
                    WHERE rooms.price_per_room <= %s AND rooms.available >= %s
                    ORDER BY rooms.price_per_room ASC
                """
                cursor.execute(query, (max_price, num_rooms_needed))
                results = cursor.fetchall()

                if results:
                    hotel_names = [
                        f"{row['Name']} - {row['Available Rooms']} rooms available - ${row['Per Room Price']}" 
                        for row in results
                    ]
                    selected_hotel = st.radio("Select a Hotel to Book:", hotel_names)
                    selected_hotel_details = next(
                        (hotel for hotel in results if f"{hotel['Name']} - {hotel['Available Rooms']} rooms available - ${hotel['Per Room Price']}" == selected_hotel),
                        None
                    )

                    if selected_hotel_details:
                        st.write(f"**Hotel Name**: {selected_hotel_details['Name']}")
                        total_price = num_rooms_needed * selected_hotel_details['Per Room Price']
                        st.write(f"Total Price: ${total_price}")

                        if st.button("Proceed to Book", key="book_by_price_room"):
                            try:
                                update_rooms_query = """
                                    UPDATE rooms
                                    SET available = available - %s
                                    WHERE hid = %s
                                """
                                cursor.execute(update_rooms_query, (num_rooms_needed, selected_hotel_details['ID']))

                                insert_booking_query = """
                                    INSERT INTO bookings (user_id, hotel_id, room_count, amount_paid, check_in_date, check_out_date)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                """
                                check_in_date = datetime.date.today()
                                check_out_date = check_in_date + datetime.timedelta(days=2)
                                cursor.execute(insert_booking_query, (user_id, selected_hotel_details['ID'], num_rooms_needed, total_price, check_in_date, check_out_date))

                                conn.commit()
                                st.success(f"You've booked {num_rooms_needed} rooms at {selected_hotel_details['Name']}! Total: ${total_price}. Proceed with payment.")
                            except Exception as e:
                                st.error(f"Booking failed: {e}")
                else:
                    st.write("No matching hotels found based on your criteria.")
            finally:
                cursor.close()
                conn.close()
