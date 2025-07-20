import streamlit as st
import pandas as pd
from utils.expense_utils import load_expenses, save_expense, clear_expenses
from utils.db import load_trips
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="SmartTravel Expense Tracker", layout="wide")

# ──────────────── Apply Custom Style ──────────────── #
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

        .stSelectbox>div>div, .stNumberInput>div>input, .stTextInput>div>input {
            background-color: var(--card-bg) !important;
            color: var(--text-color) !important;
        }

        .stDataFrame, .stTable, .stMarkdown {
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

st.title("AI-Powered Expense Tracker")

# --- Ensure user is logged in ---
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] != True:
    st.warning("Please log in from the home page to access this page.")
    st.stop()

user = st.session_state.get("username", "unknown-user")

# --- Trip Options (from saved itineraries) ---
user_trips = load_trips(user)
trip_options = sorted(set(trip["destination"] for trip in user_trips))

# --- If no trips exist, suggest planning one first ---
if not trip_options:
    st.info("You haven't planned any trips yet. Plan one to start logging expenses.")
    st.page_link("pages/Planner.py", label="Plan a Trip First")
    st.stop()

# --- Log a New Expense ---
st.subheader("Log a New Expense")
with st.form("expense_form"):
    default_trip = st.session_state.get("current_trip", {})
    default_dest = default_trip.get("destination")
    trip_index = trip_options.index(default_dest) if default_dest in trip_options else 0
    trip = st.selectbox("Trip Destination", trip_options, index=trip_index)

    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Transport", "Accommodation", "Activities", "Misc"])
    notes = st.text_input("Notes (optional)")
    date = st.date_input("Date", value=datetime.today())
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        save_expense(user, {
            "trip": trip,
            "amount": amount,
            "category": category,
            "notes": notes,
            "date": str(date)
        })
        st.success("Expense added!")

# --- View + Filter Expenses ---
st.markdown("---")
st.subheader("Expense Summary")

expenses = load_expenses(user)
if not expenses:
    st.info("No expenses recorded yet.")
    st.stop()

df = pd.DataFrame(expenses)
df["date"] = pd.to_datetime(df["date"])

# --- Filters ---
st.markdown("### Filters")
col1, col2 = st.columns(2)
with col1:
    selected_trip = st.selectbox("Filter by Trip", ["All"] + trip_options)
with col2:
    selected_category = st.selectbox("Filter by Category", ["All"] + df["category"].unique().tolist())

# --- Apply filters ---
filtered_df = df.copy()
if selected_trip != "All":
    filtered_df = filtered_df[filtered_df["trip"] == selected_trip]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

# --- Summary + Table ---
total = filtered_df["amount"].sum()
st.write(f"**Total Spent:** ₹{total:.2f}")
st.dataframe(filtered_df[["date", "trip", "category", "amount", "notes"]].sort_values(by="date", ascending=False))

# --- Pie Chart ---
if not filtered_df.empty:
    st.markdown("### Category Breakdown")
    category_totals = filtered_df.groupby("category")["amount"].sum()
    fig, ax = plt.subplots()
    ax.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

# --- Per-Trip Totals ---
st.markdown("### Per-Trip Total Expenses")
trip_totals = df.groupby("trip")["amount"].sum().reset_index()
st.table(trip_totals.rename(columns={"trip": "Trip", "amount": "Total Spent (₹)"}))

# --- Export to CSV ---
csv = filtered_df.to_csv(index=False)
st.download_button("Download Filtered Data as CSV", data=csv, file_name="expenses.csv", mime="text/csv")

# --- Clear Expenses ---
if st.button("Clear All Expenses"):
    clear_expenses(user)
    st.success("All expenses cleared.")
    st.rerun()

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