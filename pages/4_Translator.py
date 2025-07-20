import streamlit as st
import streamlit.components.v1 as components
from utils.gemini_client import ask_gemini

st.set_page_config(page_title="Chat & Translator", layout="wide")

# ──────── Custom Styling ──────── #
st.markdown("""
    <style>
        .translator-header {
            font-size: 36px;
            font-weight: 800;
            color: #0fa3b1;
            margin-bottom: 0;
        }

        .translator-sub {
            font-size: 18px;
            font-weight: 400;
            color: #a9b8c1;
            margin-bottom: 2rem;
        }

        .response-box {
            background-color: #1e2f4d;
            color: #fefefe;
            border-left: 5px solid #0fa3b1;
            border-radius: 12px;
            padding: 16px;
            margin: 10px 0;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            font-size: 16px;
        }

        .stButton>button {
            background-color: #0fa3b1;
            color: white;
            font-weight: 600;
            border-radius: 8px;
        }

        .stTextArea textarea {
            background-color: #1e2f4d;
            color: #fefefe;
            border-radius: 10px;
        }

        .stSelectbox div[data-baseweb="select"] {
            background-color: #1e2f4d;
            color: #fefefe;
            border-radius: 10px;
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
st.markdown("<div class='translator-header'> Chat & Translator</div>", unsafe_allow_html=True)
st.markdown("<div class='translator-sub'>Type in your language and get a reply in another</div>", unsafe_allow_html=True)

# ──────── Auth Check ──────── #
if "authentication_status" not in st.session_state or st.session_state["authentication_status"] != True:
    st.warning("Please log in from the home page to access this page.")
    st.stop()

user = st.session_state.get("username", "unknown-user")

# ──────── Language Selection ──────── #
source_lang = st.selectbox("Your Language", ["English", "Spanish", "French", "Japanese", "German"])
target_lang = st.selectbox("Assistant's Language", ["English", "Spanish", "French", "Japanese", "German"])

# ──────── User Input ──────── #
default_trip = st.session_state.get("current_trip", {})
default_prompt = f"Hi! I’m traveling in {default_trip.get('destination', '')}" if default_trip else ""
user_message = st.text_area(f"Type your message in {source_lang}:", value=default_prompt, height=150)

# ──────── Session Setup ──────── #
if "last_response_text" not in st.session_state:
    st.session_state["last_response_text"] = ""

# ──────── Translate & Chat ──────── #
if st.button("Translate & Chat"):
    if not user_message.strip():
        st.error("Please enter a message.")
    else:
        with st.spinner("Thinking..."):
            prompt = f"""
            You are a helpful assistant. A user sent the following message in {source_lang}:

            "{user_message}"

            Respond naturally and helpfully in {target_lang} only.
            DO NOT translate your response back into {source_lang}.
            Just reply in {target_lang} as if you're having a normal conversation.
            """

            try:
                response = ask_gemini(prompt).strip()
                st.session_state["last_response_text"] = response
                st.success("Reply generated!")
                st.markdown(f"<div class='response-box'><strong>Assistant ({target_lang}):</strong><br>{response}</div>", unsafe_allow_html=True)

                #  Auto speak once
                components.html(f"""
                    <script>
                        var msg = new SpeechSynthesisUtterance({repr(response)});
                        window.speechSynthesis.speak(msg);
                    </script>
                """, height=0)

            except Exception as e:
                st.error(f"Error: {str(e)}")

# ──────── Speak Again Button ──────── #
if st.session_state["last_response_text"]:
    st.markdown(f"<div class='response-box'><strong>Assistant ({target_lang}):</strong><br>{st.session_state['last_response_text']}</div>", unsafe_allow_html=True)

    if st.button("Speak Again"):
        components.html(f"""
            <script>
                var msg = new SpeechSynthesisUtterance({repr(st.session_state["last_response_text"])});
                window.speechSynthesis.speak(msg);
            </script>
        """, height=0)

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






