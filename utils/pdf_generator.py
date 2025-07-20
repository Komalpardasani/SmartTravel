from fpdf import FPDF
import os

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
        self.add_font("DejaVu", "", font_path, uni=True)
        self.set_font("DejaVu", size=14)

    def header(self):
        self.set_font("DejaVu", size=14)
        self.cell(0, 10, "Travel Itinerary", ln=True, align="C")

    def chapter_body(self, body):
        self.set_font("DejaVu", size=12)
        self.multi_cell(0, 8, body)
        self.ln()

def generate_pdf(trip, filename):
    pdf = PDF()
    pdf.add_page()

    body = (
        f"Destination: {trip['destination']}\n"
        f"Interests: {trip['interests']}\n"
        f"Start Date: {trip['start_date']}\n"
        f"Duration: {trip['days']} days\n"
        f"Estimated Budget/Day: ₹{trip.get('budget_per_day', 0):.2f}\n\n"
        f"{trip['itinerary']}"
    )

    pdf.chapter_body(body)
    pdf.output(filename)
    return filename





