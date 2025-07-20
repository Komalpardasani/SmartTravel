import streamlit as st
from datetime import date
import base64
import os
import re
from utils.gemini_client import ask_gemini
from utils.db import save_trip, load_trips, clear_trips, mark_favorite
from utils.pdf_generator import generate_pdf

st.set_page_config(page_title="SmartTravel Trip Planner", layout="wide")


# ──────── Custom Styles ──────── #
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

        .trip-card {
            background-color: var(--card-bg);
            color: var(--text-color);
            border-left: 5px solid var(--card-border);
            border-radius: 12px;
            padding: 16px;
            margin: 15px 0;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }

        .trip-card strong {
            color: var(--primary-color);
        }

        .stButton>button {
            background-color: var(--primary-color) !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
        }

        .stTextInput>div>input, .stNumberInput>div>input, .stDateInput input {
            background-color: var(--card-bg);
            color: var(--text-color);
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


st.markdown("<div class='header-main'>Personalized Trip Planner</div>", unsafe_allow_html=True)
st.markdown("<div class='header-sub'>Tell us your dream destination and interests, and let SmartTravel AI design the perfect itinerary</div>", unsafe_allow_html=True)

# ──────── Auth Check ──────── #
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] != True:
    st.warning("Please log in from the home page to access this page.")
    st.stop()

user = st.session_state.get("username", "unknown-user")

# ──────── Trip Planning Form ──────── #
st.subheader("Plan a New Trip")
with st.form("trip_form"):
    destination = st.text_input("Destination", "Kyoto")
    interests = st.text_input("Your Interests", "temples, culture, food")
    days = st.number_input("Trip Duration (in days)", min_value=1, max_value=30, value=3)
    trip_start = st.date_input("Trip Start Date", value=date.today())
    budget_per_day = st.number_input("Estimated Budget Per Day (₹)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Generate Travel Plan")

if submitted:
    with st.spinner("SmartTravel AI is preparing your itinerary..."):
        prompt = (
            f"Create a {days}-day travel itinerary for {destination} starting from {trip_start}. "
            f"The user is interested in {interests}. "
            f"The estimated budget per day is ₹{budget_per_day:.2f}. "
            f"Make sure the plan is fun, practical, and respects the budget."
        )
        try:
            response = ask_gemini(prompt)
            st.success("Your itinerary is ready!")
            st.markdown(response)

            save_trip(user, {
                "destination": destination,
                "interests": interests,
                "days": days,
                "start_date": str(trip_start),
                "budget_per_day": budget_per_day,
                "favorite": False,
                "itinerary": response
            })

            st.session_state["current_trip"] = {
                "destination": destination,
                "interests": interests,
                "days": days,
                "start_date": str(trip_start),
                "budget_per_day": budget_per_day,
                "gender": st.session_state.get("gender", "Prefer not to say")
            }

        except Exception as e:
            st.error(f"Error generating itinerary: {str(e)}")

# ──────── Past Trips Section ──────── #
st.markdown("---")
st.subheader("Your Saved Trips")

filter_dest = st.text_input("🔎 Search by Destination")

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("Clear All My Trips"):
        clear_trips(user)
        st.success("All your trips have been deleted.")
        st.rerun()

past_trips = load_trips(user)
filtered = [trip for trip in past_trips if filter_dest.lower() in trip["destination"].lower()]

if not filtered:
    st.info("No trips found.")
else:
    for i, trip in enumerate(reversed(filtered), 1):
        title = f"Trip #{i}: {trip['destination']} ({trip['days']} days)"
        if trip.get("favorite"):
            title += " ★"
        with st.expander(title):
            st.markdown(f"<div class='trip-card'>", unsafe_allow_html=True)
            st.write(f"**Start Date:** {trip.get('start_date', 'N/A')}")
            st.write(f"**Interests:** {trip['interests']}")
            st.write(f"**Estimated Budget/Day:** ₹{trip.get('budget_per_day', 0):.2f}")
            st.markdown("---")
            st.markdown("### Itinerary")
            st.markdown(trip["itinerary"])
            st.markdown("</div>", unsafe_allow_html=True)

            colA, colB, colC = st.columns(3)

            with colA:
                if st.button(f"{'Unfavorite' if trip.get('favorite') else 'Favorite'}", key=f"fav-{i}"):
                    mark_favorite(user, trip["destination"], not trip.get("favorite"))
                    st.rerun()

            with colB:
                filename = f"{trip['destination'].replace(' ', '_')}_itinerary.txt"
                b64 = base64.b64encode(trip["itinerary"].encode()).decode()
                href = f'<a href="data:text/plain;base64,{b64}" download="{filename}">Download as Text</a>'
                st.markdown(href, unsafe_allow_html=True)

            with colC:
                pdf_path = generate_pdf(trip, f"{trip['destination'].replace(' ', '_')}_itinerary.pdf")
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Download as PDF",
                        data=f,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                        use_container_width=True,
                        key=f"pdf-{i}"
                    )

# ──────── Navigation ──────── #
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











