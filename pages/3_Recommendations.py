import streamlit as st
from datetime import datetime
from utils.gemini_client import ask_gemini

st.set_page_config(page_title="Real-Time Recommendations", layout="wide")

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

st.markdown("<div class='header-crazy'>Real-Time Recommendations</div>", unsafe_allow_html=True)
st.markdown("<div class='header-tagline'>What to do <em>right now</em> based on your location, time, and mood!</div>", unsafe_allow_html=True)

# --- Auth check ---
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] != True:
    st.warning("Please log in from the home page to access this page.")
    st.stop()

user = st.session_state.get("username", "unknown-user")

# --- Input form ---
with st.form("recommendation_form"):
    default_trip = st.session_state.get("current_trip", {})
    city = st.text_input("Where are you now?", default_trip.get("destination", ""), placeholder="e.g., Tokyo, Paris")

    mood = st.selectbox(
        "What's your current mood?",
        ["Adventurous", "Relaxed", "Curious", "Hungry", "Romantic", "Energetic"]
    )
    now = datetime.now()
    current_hour = now.strftime("%H:%M")
    submitted = st.form_submit_button("Give Me Ideas!")

# --- Generate response ---
if submitted:
    with st.spinner("Thinking of wild, fun, and mood-matched things you can do *right now*..."):
        prompt = f"""
        You are a hyper-personalized travel assistant.

        A user is in **{city}**, the current local time is **{current_hour}**, and their mood is **{mood}**.

        Based on all 3 (location, time, mood), suggest **exactly 3** bold, fun, time-sensitive, *actionable* things they can do **right now** in {city}.

        Include **real venue names**, local experiences, time-aware context (e.g., don’t suggest morning hikes at night).

        Mood guidance:
        - Adventurous → wild, outdoor, unusual things
        - Relaxed → spas, lakes, rooftops, cafes
        - Curious → cultural, quirky, niche spots
        - Hungry → food trucks, night bites, signature dishes
        - Romantic → evening spots, lights, quiet strolls
        - Energetic → music, movement, people, parties

        Format each suggestion in this style:
        **[Short title]**: [1-line action with location name]
        """

        try:
            response = ask_gemini(prompt)
            st.success("Here's what you can do right now:")
            for line in response.strip().split("\n"):
                if line.strip():
                    st.markdown(f"<div class='recommendation-card'>{line}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

# --- Footer / Nav ---
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
