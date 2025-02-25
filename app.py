from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587  # Use 587 for TLS

def send_email(user_email):
    msg = EmailMessage()
    msg["Subject"] = "New Case Study Submission"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content(f"A new case study has been submitted by {user_email}.")

    # Send Email via Outlook SMTP
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()  # Secure the connection
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("Email Sent!")

@app.route("/", methods=["GET"])
def home():
    return "Flask app is running!", 200

@app.route("/submit", methods=["POST"])
def handle_form():
    data = request.form.to_dict()
    
    # Send email notification
    send_email(data.get("email"))

    return jsonify({"message": "Case study submitted successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
