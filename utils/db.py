import json
import os
from datetime import datetime

TRIPS_FILE = os.path.join("data", "trips.json")
BOOKINGS_FILE = os.path.join("data", "bookings.json")

def load_all_trips():
    if not os.path.exists(TRIPS_FILE):
        return {}
    with open(TRIPS_FILE, "r") as f:
        return json.load(f)

def load_trips(user_email):
    all_trips = load_all_trips()
    return all_trips.get(user_email, [])

def save_trip(user_email, trip):
    all_trips = load_all_trips()
    if user_email not in all_trips:
        all_trips[user_email] = []
    all_trips[user_email].append(trip)
    with open(TRIPS_FILE, "w") as f:
        json.dump(all_trips, f, indent=2)

def clear_trips(user_email):
    all_trips = load_all_trips()
    if user_email in all_trips:
        all_trips[user_email] = []
    with open(TRIPS_FILE, "w") as f:
        json.dump(all_trips, f, indent=2)

def mark_favorite(user_email, destination, favorite_status):
    all_trips = load_all_trips()
    trips = all_trips.get(user_email, [])
    for trip in trips:
        if trip["destination"] == destination:
            trip["favorite"] = favorite_status
    with open(TRIPS_FILE, "w") as f:
        json.dump(all_trips, f, indent=2)

def save_booking(user, booking_data):
    # Load existing bookings
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "r") as f:
            bookings = json.load(f)
    else:
        bookings = {}

    if user not in bookings:
        bookings[user] = []

    booking_data["booked_on"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    bookings[user].append(booking_data)

    # Save back to file
    with open(BOOKINGS_FILE, "w") as f:
        json.dump(bookings, f, indent=4)

    print("Booking saved:", booking_data)



