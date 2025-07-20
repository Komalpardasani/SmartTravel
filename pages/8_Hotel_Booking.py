import streamlit as st
from utils.gemini_client import ask_gemini
from utils.db import save_booking
from datetime import datetime, timedelta
import re

st.set_page_config(page_title="Hotel Booking", layout="wide")

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

        .hotel-card {
            background-color: var(--card-bg);
            color: var(--text-color);
            border-left: 5px solid var(--primary-color);
            border-radius: 12px;
            padding: 16px;
            margin: 10px 0;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            font-size: 16px;
        }

        .hotel-card strong {
            color: var(--primary-color);
        }

        .header-main {
            font-size: 36px;
            font-weight: 800;
            color: var(--primary-color);
            margin-bottom: 0;
        }

        .header-sub {
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

st.markdown("<div class='header-main'>Hotel Booking</div>", unsafe_allow_html=True)
st.markdown("<div class='header-sub'>Curated listings tailored to your destination and travel plans</div>", unsafe_allow_html=True)

# ──────── Auth Check ──────── #
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] != True:
    st.warning("Please log in from the home page to access this page.")
    st.stop()

user = st.session_state.get("username", "unknown-user")
trip = st.session_state.get("current_trip", {})

# ──────── Inputs ──────── #
city = st.text_input("Destination City", trip.get("destination", ""))
start_date = st.date_input("Check-in Date", datetime.strptime(trip.get("start_date", str(datetime.today().date())), "%Y-%m-%d"))
days = st.number_input("Number of Nights", min_value=1, max_value=30, value=trip.get("days", 3))
budget = st.number_input("Estimated Budget per Night (₹)", min_value=500.0, max_value=10000.0, value=float(trip.get("budget_per_day", 4000.0)))

checkout_date = start_date + timedelta(days=days)
st.write(f"**Stay Duration:** {start_date.strftime('%Y-%m-%d')} → {checkout_date.strftime('%Y-%m-%d')}")

# ──────── AI Recommendations ──────── #
if st.button("Find Hotels"):
    with st.spinner("Looking for top-rated hotels..."):
        prompt = f"""
Generate 3 **fictional but realistic** hotel listings in {city} for a {days}-night stay starting on {start_date.strftime('%Y-%m-%d')}. Budget: ₹{budget} per night.

Each hotel should include:

- **Hotel Name** (bold)
- Price per night in INR
- Star rating (1-5★)
- Amenities (e.g., Wi-Fi, AC, Breakfast)
- Distance from city center or a tourist spot

Only return clean markdown listings. Do **NOT** add disclaimers, real-time accuracy warnings, or booking advice. This is for a mock booking UI only.
"""
        try:
            response = ask_gemini(prompt)
            st.success("Top hotel recommendations:")
            hotels = re.split(r"\n(?=\*\*)", response.strip())

            for i, hotel in enumerate(hotels):
                if hotel.strip():
                    st.markdown(f"<div class='hotel-card'>{hotel.strip()}</div>", unsafe_allow_html=True)
                    if st.button("Book This Hotel", key=f"book_hotel_{i}"):
                        booking = {
                            "type": "hotel",
                            "destination": city,
                            "checkin_date": start_date.strftime('%Y-%m-%d'),
                            "checkout_date": checkout_date.strftime('%Y-%m-%d'),
                            "details": hotel.strip()
                        }
                        save_booking(user, booking)
                        st.session_state["selected_hotel"] = booking
                        st.success("Hotel booked and saved successfully!")
        except Exception as e:
            st.error(f"Error generating hotel list: {str(e)}")

# ──────── Navigation ──────── #
st.markdown("---")
st.markdown("### Navigate to Other Tools")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/1_Planner.py", label="Trip Planner")
    st.page_link("pages/7_Flight_Booking.py", label="Flight Booking")
    st.page_link("pages/8_Hotel_Booking.py", label="Hotel Booking")

with col2:
    st.page_link("pages/6_Packing_Assistant.py", label="AI Packing Assistant")
    st.page_link("pages/5_Safety.py", label="Emergency & Safety Tools")
    st.page_link("pages/4_Translator.py", label="AI Chat & Translator")

with col3:
    st.page_link("pages/3_Recommendations.py", label="Recommendations")
    st.page_link("pages/2_Expense_Tracker.py", label="Expense Tracker")