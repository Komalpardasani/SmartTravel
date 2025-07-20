import streamlit as st
import re
import os
import json
from PIL import Image
from utils.auth_utils import register_user, authenticate_user
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"


st.set_page_config(page_title="SmartTravel Assistant", layout="wide")

# ──────────────── Hide Sidebar on Login Screen ──────────────── #
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = False

if not st.session_state["authentication_status"]:
    st.markdown("""
        <style>
            [data-testid="collapsedControl"] {
                display: none;
            }
            section[data-testid="stSidebar"] {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

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
                --card-bg: #f3f9fb;
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

        .custom-header {
            font-size: 42px;
            font-weight: 900;
            color: var(--primary-color);
            margin-bottom: 0.2rem;
            animation: fadeSlide 1.2s ease-in-out;
        }

        @keyframes fadeSlide {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        .custom-subheader {
            font-size: 20px;
            font-weight: 400;
            color: #a9b8c1;
        }

        .greeting-banner {
            background: linear-gradient(to right, #e0f7fa, #e0f2f1);
            padding: 24px;
            border-radius: 14px;
            margin-bottom: 24px;
            color: #004d40;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
        }

        .greeting-banner h3 {
            font-size: 26px;
            font-weight: 700;
        }

        .greeting-banner p {
            font-size: 16px;
            margin: 0;
        }

        .card-wrapper {
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .card {
            background-color: var(--card-bg);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid var(--card-border);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            height: 190px;
        }

        .card:hover {
            transform: translateY(-6px);
            box-shadow: 0 10px 22px rgba(0,0,0,0.5);
        }

        .card h4 {
            color: var(--primary-color);
            font-size: 20px;
        }

        .card p {
            color: var(--text-color);
            font-size: 15px;
        }

        .stButton button {
            width: 100%;
            background-color: var(--primary-color) !important;
            color: white !important;
            font-weight: 700 !important;
            border-radius: 10px !important;
            padding: 12px 0 !important;
            margin-top: 8px;
        }

        .trip-history-box {
            background-color: #ffffff;
            border: 3px solid var(--primary-color);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }

        .trip-history-box div {
            color: #1e2f4d;
        }

        .stPageLinkButton button {
            width: 100%;
            background-color: var(--primary-color) !important;
            color: white !important;
            font-weight: 700 !important;
            border-radius: 10px !important;
            padding: 10px 0 !important;
            margin-top: 12px !important;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }

        .stPageLinkButton button:hover {
            background-color: #009fcc !important;
            transform: translateY(-3px);
        }

    </style>
            
""", unsafe_allow_html=True)


# ──────────────── Auth State ──────────────── #
for key in ["username", "name"]:
    if key not in st.session_state:
        st.session_state[key] = None

auth_status = st.session_state["authentication_status"]
username = st.session_state["username"]
name = st.session_state["name"]

# ──────────────── Branding ──────────────── #
def show_logo_and_header():
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("logo.png", width=140)
    with col2:
        st.markdown('<div class="custom-header">SmartTravel Assistant</div>', unsafe_allow_html=True)
        st.markdown('<div class="custom-subheader">Effortless trip planning with AI-powered insights.</div>', unsafe_allow_html=True)


# ──────────────── Login / Signup ──────────────── #
if not auth_status:
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:
        st.subheader("Login to SmartTravel")
        login_email = st.text_input("Email", key="login_email")
        login_pass = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            login_email = login_email.strip().lower()
            user_name = authenticate_user(login_email, login_pass)
            if user_name:
                st.session_state.update({
                    "authentication_status": True,
                    "username": login_email,
                    "name": user_name,
                })
                st.rerun()
            else:
                st.error("Invalid email or password.")

    with signup_tab:
        st.subheader("Create a New Account")
        new_name = st.text_input("Full Name", key="signup_name")
        new_email = st.text_input("Email", key="signup_email")
        new_pass = st.text_input("Password", type="password", key="signup_password")
        confirm_pass = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

        if st.button("Sign Up"):
            new_email = new_email.strip().lower()
            if not new_name or not new_email or not new_pass or not confirm_pass:
                st.error("All fields are required.")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                st.error("Please enter a valid email.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            elif len(new_pass) < 8 or not re.search(r"[A-Z]", new_pass) or not re.search(r"[a-z]", new_pass) or not re.search(r"\d", new_pass):
                st.error("Password must be at least 8 characters with a number, lowercase and uppercase letter.")
            elif register_user(new_email, new_pass, new_name):
                st.success("Account created! Logging you in...")
                st.session_state.update({
                    "authentication_status": True,
                    "username": new_email,
                    "name": new_name,
                })
                st.rerun()
            else:
                st.warning("An account with this email already exists.")

# ──────────────── Dashboard ──────────────── #
if auth_status:
    st.sidebar.success(f"Logged in as {name}")
    if st.sidebar.button("Logout"):
        st.session_state["authentication_status"] = False
        st.session_state["username"] = None
        st.session_state["name"] = None
        st.rerun()

    show_logo_and_header()
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust the ratio as needed
    with col2:
        st.image("travel.jpg", width=900)

    st.markdown("""
        <div class="greeting-banner">
            <h3>Welcome to your SmartTravel Dashboard</h3>
            <p>Plan, manage, and optimize your travel experience with ease.</p>
        </div>
    """, unsafe_allow_html=True)

    card_data = [
        ("Trip Planner", "Create custom itineraries based on interests.", "pages/1_Planner.py", "fa-route"),
        ("Expense Tracker", "Log and analyze your trip expenses by category.", "pages/2_Expense_Tracker.py", "fa-wallet"),
        ("Recommendations", "Get smart tips and hidden gems for your trip.", "pages/3_Recommendations.py", "fa-lightbulb"),
        ("AI Chat & Translator", "Translation with natural language AI assistant.", "pages/4_Translator.py", "fa-language"),
        ("Emergency & Safety Tools", "Access local contacts and stay alert to danger zones.", "pages/5_Safety.py", "fa-triangle-exclamation"),
        ("AI Packing Assistant", "Smart packing lists based on destination and weather.", "pages/6_Packing_Assistant.py", "fa-suitcase-rolling"),
        ("Flight Booking", "Find affordable flights to your destination.", "pages/7_Flight_Booking.py", "fa-plane-departure"),
        ("Hotel Booking", "Browse hotel stays for your travel dates.", "pages/8_Hotel_Booking.py", "fa-hotel")

    ]

    for i in range(0, len(card_data), 3):
        cols = st.columns(3)
        for idx, (title, desc, path, icon) in enumerate(card_data[i:i+3]):
            with cols[idx]:
                st.markdown(f"""
                            <div class="card-wrapper">
                            <div class="card">
                                <h4><i class="fa-solid {icon}" style="margin-right: 8px; color: #dab3ff;"></i>{title}</h4>
                                <p>{desc}</p>
                """, unsafe_allow_html=True)

                # Place the Open button **inside** the .card
                if st.button("Open", key=f"open_{path}"):
                    st.switch_page(path)

                st.markdown("""
                        </div>
                    </div>
                """, unsafe_allow_html=True)



    st.markdown("### Your Travel History")
    st.markdown("View your previous planned trips and explore them again!")

    trip_file_path = os.path.join("data", "trips.json")
    try:
        with open(trip_file_path, "r") as f:
            trips_data = json.load(f)
    except FileNotFoundError:
        trips_data = {}

    user_trips = trips_data.get(st.session_state["username"], [])

    if user_trips:
        for trip in user_trips[::-1]:
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"""
                        <div class='trip-history-box'>
                            <div style='font-size: 20px; font-weight: bold;'>
                                {trip['destination']}
                            </div>
                            <div style='font-size: 15px;'>
                                {trip['start_date']} • {trip['days']} days • ₹{trip['budget_per_day']} per day
                            </div>
                            <div style='margin-top: 8px; font-size: 14px;'>
                                <strong>Interests:</strong> {trip['interests']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("View Itinerary", key=f"{trip['destination']}_{trip['start_date']}"):
                        st.session_state["selected_trip"] = trip
                        st.switch_page("pages/Planner.py")
    else:
        st.info("No past trips found. Start planning to see your history here!")




