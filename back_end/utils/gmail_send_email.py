import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

# Path to the client secret file
CLIENT_SECRET_FILE = 'client_secret.json'

# Define the scopes for the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

def send_email(to, subject, body):
    """Send an email message.

    Args:
        to (str): The email address of the recipient.
        subject (str): The subject of the email.
        body (str): The body of the email.
    """
    try:
        # Authenticate with the Gmail API
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('gmail', 'v1', credentials=creds)

        # Construct the email message
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        body_content = MIMEText(body, 'html')
        message.attach(body_content)
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        
        # Send the email message
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {to} Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message

to = 'jenniejing@gmail.com'
subject = 'Test Email'
body = '<h1>This is a test email sent via Python!</h1>'
send_email(to, subject, body)