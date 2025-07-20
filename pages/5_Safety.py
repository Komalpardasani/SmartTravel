import streamlit as st
from utils.gemini_client import ask_gemini

st.set_page_config(page_title="Travel Safety & Emergency Info", layout="wide")

# ──────── Enhanced Styling ──────── #
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #0d1b2a, #1b263b);
            color: #fefefe;
            font-family: 'Segoe UI', sans-serif;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .header-main {
            font-size: 42px;
            font-weight: 800;
            color: #0fa3b1;
            margin-bottom: 0.3rem;
            text-align: left;
        }

        .header-sub {
            font-size: 18px;
            font-weight: 400;
            color: #ced4da;
            margin-bottom: 2.5rem;
            text-align: left;
        }

        .safety-card {
            background-color: #1e2f4d;
            color: #fefefe;
            border-left: 5px solid #0fa3b1;
            border-radius: 14px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            transition: transform 0.3s ease;
        }

        .safety-card:hover {
            transform: scale(1.02);
        }

        .safety-card strong {
            color: #0fa3b1;
        }

        .stButton>button {
            background-color: #0fa3b1;
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 0.5rem 1.2rem;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }

        .stButton>button:hover {
            background-color: #0c8791;
            transform: scale(1.02);
        }

        .stTextInput>div>input {
            background-color: #1e2f4d;
            color: #fefefe;
            border-radius: 8px;
        }

        .stTextInput>div>input::placeholder {
            color: #9ca3af;
        }

        .stPageLink {
            padding: 12px 20px;
            background-color: #1e2f4d;
            border-radius: 10px;
            font-weight: 600;
            color: #ffffff !important;
            display: block;
            text-decoration: none !important;
            margin-bottom: 12px;
            transition: background-color 0.3s ease, transform 0.2s ease;
            text-align: center;
        }
        .stPageLink span {
            color: #ffffff !important;  /* Force inner text color */
        }

        .stPageLink:hover {
            background-color: #0fa3b1;
            color: #ffffff !important;
            transform: scale(1.02);
        }
    </style>
""", unsafe_allow_html=True)

# ──────── Header ──────── #
st.markdown("<div class='header-main'>Travel Safety & Emergency Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='header-sub'>Get smart, up-to-date safety guidance and emergency help for your destination</div>", unsafe_allow_html=True)

# ──────── Auth Check ──────── #
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] != True:
    st.warning("Please log in from the home page to access this page.")
    st.stop()

user = st.session_state.get("username", "unknown-user")

# ──────── Input ──────── #
default_trip = st.session_state.get("current_trip", {})
city = st.text_input("Enter your travel destination", default_trip.get("destination", ""), placeholder="e.g., Tokyo")

# ──────── Safety Info Fetch ──────── #
if st.button("Get Safety Info"):
    with st.spinner("Fetching safety recommendations..."):
        prompt = f"""
I'm planning a trip to {city}.
Please provide the most recent and location-specific safety and emergency information, including:

1. The latest verified **emergency contact numbers** for:
   - Police
   - Ambulance
   - Tourist helplines (if available)

2. Known **dangerous areas or neighborhoods** (especially after dark) that travelers should avoid, try providing specific location names in the city.

3. **Recent travel safety alerts, local scams, or crime trends** relevant to tourists, and if possible, provide some particular locations to be more cautious.

4. Addresses or phone numbers of **local police stations** or emergency services in that city. Provide a general contact number for the city, irrespective of local location.

5. Any **local apps, hotlines, or government portals** available for safety or emergency support.

Please ensure the data is current and location-specific. If something is uncertain, mention that it may vary or suggest checking with local authorities.
Make the response well-structured and easy to scan quickly.
"""
        try:
            response = ask_gemini(prompt)
            st.success("Safety info retrieved!")
            st.markdown(f"<div class='safety-card'>{response}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ──────── Navigation Footer ──────── #
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
