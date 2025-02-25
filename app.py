from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# Environment Variables for Email Configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER")  # Sender's email (e.g., casestudy19877@gmail.com)
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # App password for the sender (if 2FA is enabled)
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")  # Receiver's email (e.g., keira.jarvis@hotmail.co.uk)

SMTP_SERVER = "smtp.gmail.com"  # Correct SMTP for Gmail
SMTP_PORT = 587  # Use 587 for TLS

def send_email(user_email):
    """Function to send an email when a form is submitted."""
    
    # Ensure EMAIL_SENDER is correctly set
    if not EMAIL_SENDER:
        print("Error: EMAIL_SENDER is not set.")
        return
    
    msg = EmailMessage()
    msg["Subject"] = "New Case Study Submission"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content(f"A new case study has been submitted by {user_email}.")

    try:
        # Connect to Gmail SMTP Server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()  # Secure the connection
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)  # Login with Gmail credentials
            smtp.send_message(msg)
        print("✅ Email Sent Successfully!")

    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication Error: {e}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")


@app.route("/", methods=["GET"])
def home():
    return "Flask app is running!", 200


@app.route("/submit", methods=["POST"])
def handle_form():
    """Handles form submissions from the frontend."""
    data = request.form.to_dict()

    if "email" not in data or not data["email"]:
        return jsonify({"error": "Email field is required!"}), 400

    # Send email notification
    send_email(data.get("email"))

    return jsonify({"message": "✅ Case study submitted successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True)
