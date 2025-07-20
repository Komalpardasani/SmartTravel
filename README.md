
#  SmartTravel: Your Personalized AI-Powered Travel Companion

SmartTravel is a powerful AI-integrated travel assistant built using Streamlit and Google Gemini. From personalized itineraries to multilingual translation and safety tips, it combines multiple tools into a single seamless dashboard for travelers.

---

<p align="center">
  <img src="logo.png" alt="SmartTravel Logo"/>
</p>

##  Features

- **Trip Planner:** Personalized itineraries based on interests, duration, and budget.
- **Expense Tracker:** Log, filter, and visualize trip expenses with pie charts and export options.
- **Real-Time Recommendations:** AI-powered suggestions based on location, mood, and time.
- **Translator + AI Chat:** Talk to AI in multiple languages with voice playback support.
- **Travel Safety:** Emergency contacts, scams to watch for, and local alerts powered by AI.
- **Packing Assistant:** AI-generated packing lists based on weather, gender, and destination.
- **Flight & Hotel Booking:** Seamlessly search and reserve flights and accommodations customized to your travel plans.


---

##  Powered by Gemini AI

SmartTravel integrates Google's `gemini-1.5-pro` to provide:
- Realistic trip itineraries
- Interactive travel suggestions
- Conversational translations
- AI-driven local insights

---


##  Setup Instructions

###  Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Komalpardasani/SmartTravel.git
cd SmartTravel
```

2. **Create and activate a virtual environment**

On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Create a `.env` file in the project root directory**

Add your Gemini API key like this:
```env
GEMINI_API_KEY=your-gemini-api-key
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the app**
```bash
streamlit run main.py
```


---

##  Tech Stack

- **Framework:** Streamlit
- **AI:** Google Generative AI (Gemini)
- **Backend:** Python
- **Data:** JSON-based local storage
- **Deployment:** Streamlit Community Cloud

## Live Demo

Access the app here: [https://smarttravel-qxkibvsg3kcfrom3hv37tx.streamlit.app/](https://smarttravel-qxkibvsg3kcfrom3hv37tx.streamlit.app/)



