import streamlit as st
from utils.gemini_client import ask_gemini
from datetime import datetime

st.set_page_config(page_title="AI Packing Assistant", layout="wide")

# ──────────────── Apply Custom Style ──────────────── #
st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #111927;
            color: #fefefe;
            font-family: 'Segoe UI', sans-serif;
        }

        .block-container {
            padding-top: 2rem;
        }

        .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
            color: #0fa3b1;
        }

        .stButton>button {
            background-color: #0fa3b1;
            color: white;
            font-weight: 600;
            border-radius: 5px;
        }

        .stSelectbox>div>div, .stNumberInput>div>input, .stTextInput>div>input {
            background-color: #1e2f4d !important;
            color: #fefefe !important;
        }

        .stMarkdown {
            color: #fefefe;
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

st.markdown("<h1>AI Packing Assistant</h1>", unsafe_allow_html=True)

# --- Ensure user is logged in ---
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] != True:
    st.warning("Please log in from the home page to access this page.")
    st.stop()

user = st.session_state.get("username", "unknown-user")

# --- Trip Info Input ---
default_trip = st.session_state.get("current_trip", {})
destination = st.text_input("Where are you traveling to?", default_trip.get("destination", ""))
duration = st.number_input("Trip duration (in days)", min_value=1, max_value=60, value=default_trip.get("days", 7))
gender_options = ["Prefer not to say", "Male", "Female", "Other"]
gender_index = gender_options.index(default_trip.get("gender", "Prefer not to say"))
gender = st.selectbox("Your gender (for clothing suggestions)", gender_options, index=gender_index)


now = datetime.now()
date_string = now.strftime('%B %d, %Y')

# --- Link to Planner if user wants more guidance ---
if destination.strip() == "":
    st.info("Want a full itinerary to guide your packing?")
    st.page_link("pages/1_Planner.py", label="Go to Trip Planner")

# --- Packing List Generation ---
if st.button("Generate Packing List"):
    with st.spinner("Inferring season and generating packing list..."):

        season_prompt = f"""
        Today is {date_string}. I'm planning to travel to {destination}.
        Please accurately determine the current season (Summer, Winter, Spring, Autumn)
        at the destination based on its geographical location and hemisphere.
        Output just one word only.
        """

        try:
            season_response = ask_gemini(season_prompt).strip().split()[0].capitalize()
            valid_seasons = ["Summer", "Winter", "Spring", "Autumn", "Wet", "Dry"]
            season = season_response if season_response in valid_seasons else "Unknown"
            st.info(f"Inferred season for {destination}: **{season}**")
        except Exception as e:
            season = "Unknown"
            st.warning(f"Could not determine season. Defaulting to 'Unknown'. ({str(e)})")

        packing_prompt = f"""
        I'm traveling to {destination} for {duration} days.
        My current local date is {date_string}, and the expected season is {season.lower()}.
        I identify as {gender.lower()}.

        Generate a packing list considering:
        - Local cultural dress norms
        - Weather-appropriate clothing for {season}
        - Essentials for a {duration}-day trip
        - Tech, health, safety, and documents
        - Optional items and what not to pack

        Organize the list by categories:
        - Clothing
        - Toiletries
        - Documents
        - Electronics
        - Medications
        - Travel Tips
        """

        try:
            packing_response = ask_gemini(packing_prompt)
            st.success(f"Packing list for {destination} ({season}) is ready!")
            try:
                st.markdown(packing_response)
            except:
                st.warning("Couldn't render the response. Showing raw output instead:")
                st.code(packing_response, language="markdown")

        except Exception as e:
            st.error(f"Error generating packing list: {str(e)}")

# --- Navigation ---
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