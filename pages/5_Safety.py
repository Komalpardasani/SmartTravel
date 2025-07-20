import streamlit as st
from utils.gemini_client import ask_gemini

st.set_page_config(page_title="Travel Safety & Emergency Info", layout="wide")

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

        .stButton>button {
            background-color: var(--primary-color) !important;
            color: white !important;
            font-weight: bold;
            border-radius: 10px;
        }

        .safety-card {
           background-color: var(--card-bg);
           color: var(--text-color);
           border-left: 5px solid var(--primary-color);
           border-radius: 12px;
           padding: 16px;
           margin: 10px 0;
           box-shadow: 0 4px 10px rgba(0,0,0,0.3);
           font-size: 16px;
        }

        .safety-card strong {
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

# ──────────────── Header ──────────────── #
st.markdown("<div class='header-main'>Travel Safety & Emergency Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='header-sub'>Get smart, up-to-date safety guidance and emergency help for your destination</div>", unsafe_allow_html=True)

# --- Auth check ---
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] != True:
    st.warning("Please log in from the home page to access this page.")
    st.stop()

user = st.session_state.get("username", "unknown-user")

# --- Input Form ---
default_trip = st.session_state.get("current_trip", {})
with st.form("safety_form"):
    city = st.text_input("Enter your travel destination", default_trip.get("destination", ""), placeholder="e.g., Tokyo")
    submitted = st.form_submit_button("Get Safety Info")

# --- Fetch Safety Info ---
if submitted:
    with st.spinner("Fetching safety recommendations..."):
        prompt = f"""
I'm planning a trip to {city}.
Please provide the most recent and location-specific safety and emergency information, including:

1. Emergency contact numbers (police, ambulance, tourist helplines)
2. Dangerous areas to avoid (especially after dark)
3. Recent travel safety alerts or scams
4. Local police station addresses or numbers
5. Any apps or websites for safety help

Keep it concise, structured, and easy to scan.
"""
        try:
            response = ask_gemini(prompt)
            st.success("Safety info retrieved!")
            st.markdown(f"<div class='safety-card'>{response}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")

# --- Navigation ---
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