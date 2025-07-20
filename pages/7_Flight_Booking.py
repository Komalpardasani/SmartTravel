import streamlit as st
from utils.gemini_client import ask_gemini
from utils.db import save_booking
from datetime import datetime, timedelta
import re

st.set_page_config(page_title="Flight Booking", layout="wide")

# ──────────────── Custom Styling ──────────────── #
st.markdown("""
    <style>
        :root {
            color-scheme: light dark;
        }

        body {
            background-color: var(--background-color, #111927);
            color: var(--text-color, #fefefe);
            font-family: 'Segoe UI', sans-serif;
        }

        @media (prefers-color-scheme: light) {
            body {
                --primary-color: #0fa3b1;
                --text-color: #111927;
                --background-color: #ffffff;
                --card-bg: #c6e8f4;
                --card-border: #0fa3b1;
            }
        }

        @media (prefers-color-scheme: dark) {
            body {
                --primary-color: #00c6ff;
                --text-color: #fefefe;
                --background-color: #111927;
                --card-bg: #1e2f4d;
                --card-border: #00c6ff;
            }
        }

        .block-container {
            padding-top: 2rem;
        }

        .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
            color: var(--primary-color);
        }

        .stButton>button, .stDownloadButton button {
            background-color: var(--primary-color) !important;
            color: white !important;
            font-weight: bold;
            border-radius: 10px;
        }

        .recommendation-card {
           background-color: var(--card-bg);
           color: var(--text-color);
           border-left: 5px solid var(--primary-color);
           border-radius: 12px;
           padding: 16px;
           margin: 10px 0;
           box-shadow: 0 4px 10px rgba(0,0,0,0.3);
           font-size: 16px;
        }

        .recommendation-card strong {
            color: var(--primary-color);
        }

        .header-crazy {
            font-size: 36px;
            font-weight: 800;
            color: var(--primary-color);
            margin-bottom: 0;
        }

        .header-tagline {
            font-size: 18px;
            font-weight: 400;
            color: #a9b8c1;
            margin-bottom: 2rem;
        }

        .stPageLink {
            padding: 12px 20px;
            background-color: var(--card-bg);
            border-radius: 10px;
            font-weight: 600;
            color: var(--text-color) !important;
            display: block;
            text-decoration: none !important;
            margin-bottom: 12px;
            transition: background-color 0.3s ease, transform 0.2s ease;
            text-align: center;
        }

        .stPageLink span {
            color: var(--text-color) !important;
        }

        .stPageLink:hover {
            background-color: var(--primary-color);
            color: #ffffff !important;
            transform: scale(1.02);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='header-crazy'>Flight Booking</div>", unsafe_allow_html=True)
st.markdown("<div class='header-tagline'>Find the best flights tailored to your trip</div>", unsafe_allow_html=True)

# --- Auth Check ---
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] != True:
    st.warning("Please log in from the home page to access this page.")
    st.stop()

user = st.session_state.get("username", "unknown-user")
trip = st.session_state.get("current_trip", {})

# --- Input Section ---
from_city = st.text_input("From (departure city)", trip.get("from_city", "New Delhi"))
to_city = st.text_input("To (destination city)", trip.get("destination", ""))
start_date = st.date_input("Departure Date", datetime.strptime(trip.get("start_date", str(datetime.today().date())), "%Y-%m-%d"))
days = st.number_input("Trip Duration (in days)", min_value=1, max_value=30, value=trip.get("days", 3))
return_date = start_date + timedelta(days=days)

st.write(f" **Departure:** {start_date.strftime('%Y-%m-%d')} |  **Return:** {return_date.strftime('%Y-%m-%d')}")

# --- Flight Generator ---
if st.button("Find Flights"):
    with st.spinner("Searching for best Gemini-powered flight options..."):
        prompt = f"""
Generate 3 **fictional but realistic** flight options for a traveler going from {from_city} to {to_city}.

Departure: {start_date.strftime('%Y-%m-%d')}  
Return: {return_date.strftime('%Y-%m-%d')}  
The traveler wants affordable, common airline options for this route.

You are NOT providing real-time flight data — just simulate **plausible examples** with realistic details.

For each flight, return in markdown:
- **Airline Name (Flight Number)**
- Departure and Arrival Time
- Duration
- Stops (Non-stop or via)
- Hypothetical Price in INR
- 1 line of amenities (like meals, baggage, Wi-Fi)

Do NOT include disclaimers or real booking links. Just 3 fictional listings.
"""
        try:
            response = ask_gemini(prompt)
            st.success("Here are your flight options:")

            flights = re.split(r"\n(?=\*\*)", response.strip())
            for i, flight in enumerate(flights):
                if flight.strip():
                    st.markdown(f"<div class='recommendation-card'>{flight.strip()}</div>", unsafe_allow_html=True)

                    book_key = f"booked_{i}"
                    trigger_key = f"trigger_{i}"

                    if st.button("Book This Flight", key=trigger_key):
                        st.session_state[book_key] = True

                    if st.session_state.get(book_key):
                        booking = {
                            "type": "flight",
                            "from": from_city,
                            "to": to_city,
                            "departure_date": start_date.strftime('%Y-%m-%d'),
                            "return_date": return_date.strftime('%Y-%m-%d'),
                            "details": flight.strip()
                        }
                        save_booking(user, booking)
                        st.session_state["selected_flight"] = booking
                        st.success("Booking confirmed and saved!")
                        st.session_state[book_key] = False

        except Exception as e:
            st.error(f"Error generating flight options: {str(e)}")

# --- Footer Navigation ---
st.markdown("---")
st.markdown("### Navigate to Other Tools")

col1, col2, col3 = st.columns(3)

# Column 1 – Planning & Booking
with col1:
    st.page_link("pages/1_Planner.py", label="Trip Planner")
    st.page_link("pages/7_Flight_Booking.py", label="Flight Booking")
    st.page_link("pages/8_Hotel_Booking.py", label="Hotel Booking")

# Column 2 – Preparation & Safety
with col2:
    st.page_link("pages/6_Packing_Assistant.py", label="AI Packing Assistant")
    st.page_link("pages/5_Safety.py", label="Emergency & Safety Tools")
    st.page_link("pages/4_Translator.py", label="AI Chat & Translator")

# Column 3 – In-Trip Experience & Tracking
with col3:
    st.page_link("pages/3_Recommendations.py", label="Recommendations")
    st.page_link("pages/2_Expense_Tracker.py", label="Expense Tracker")
