import os
import base64
from flask import Flask, redirect, request, jsonify
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# OAuth 2.0 credentials
CLIENT_SECRET_FILE = 'credentials.json'  # Path to your credentials JSON file
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Step 1: OAuth 2.0 flow to authenticate the user
def authenticate_gmail():
    # Create the flow using the client secrets file and the desired scopes
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, SCOPES)
    
    # Define the redirect URI that Google will use to send the user after they sign in
    flow.redirect_uri = 'https://skills-bootcamp-form-backend.onrender.com/oauth2callback'  # Update this for your deployment URL
    
    # Get the authorization URL and state
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')
    
    return authorization_url

# Step 2: Gmail API call to send email
def send_email_via_gmail(user_email, subject, body):
    # Authenticate and get the credentials
    creds = authenticate_gmail()
    
    # Build the service object for the Gmail API
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)
    
    # Create the email message
    message = MIMEMultipart()
    message['to'] = user_email
    message['subject'] = subject
    msg = MIMEText(body)
    message.attach(msg)
    
    # Encode the message in base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        # Send the email
        send_message = service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
        print(f'Message sent: {send_message["id"]}')
    except googleapiclient.errors.HttpError as error:
        print(f'An error occurred: {error}')

# Route to trigger OAuth flow (the user clicks to authorize)
@app.route('/authorize')
def authorize():
    authorization_url = authenticate_gmail()
    return redirect(authorization_url)

# Callback route to handle the response after the user authenticates
@app.route('/oauth2callback')
def oauth2callback():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, SCOPES)
    flow.redirect_uri = 'https://skills-bootcamp-form-backend.onrender.com/oauth2callback'  # Update with your Render URI
    
    # Fetch the token using the authorization response
    flow.fetch_token(authorization_response=request.url)
    
    # Save credentials to a session or file
    creds = flow.credentials
    print('Authentication successful!')
    
    # Now you can use the Gmail API to send emails
    
    return 'Authentication successful. You can now send emails.'

# Route to send the email
@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    user_email = data.get('email')
    subject = data.get('subject')
    body = data.get('body')

    if not user_email or not subject or not body:
        return jsonify({"error": "Missing required parameters"}), 400

    send_email_via_gmail(user_email, subject, body)
    return jsonify({"message": "Email sent successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
