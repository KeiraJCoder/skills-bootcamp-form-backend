import smtplib
from email.message import EmailMessage
import os

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587  # Use 587 for TLS

def send_email(pdf_path, user_email):
    msg = EmailMessage()
    msg["Subject"] = "New Case Study Submission"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content(f"A new case study has been submitted by {user_email}. See the attached PDF.")

    # Attach the PDF
    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="Case_Study.pdf")

    # Send Email via Outlook SMTP
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()  # Secure the connection
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("Email Sent!")
