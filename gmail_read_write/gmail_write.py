from __future__ import print_function
import os
import base64

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

# Use modify scope (allows read + write + create drafts)
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_service():
    """Authenticate Gmail API and return service object."""
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
    "gmail_read_write/credentials.json",
    SCOPES
)

        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


# ---------------------------------------------------------
# 1) NORMAL DRAFT (NOT REPLY)
# ---------------------------------------------------------
def create_draft(recipient, subject, body):
    """Create a new Gmail draft message."""
    service = get_service()

    message = MIMEText(body, "plain")
    message["to"] = recipient
    message["subject"] = subject

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode("utf-8")

    draft_body = {
        "message": {
            "raw": encoded_message
        }
    }

    draft = service.users().drafts().create(
        userId="me",
        body=draft_body
    ).execute()

    print("Draft created successfully!")
    return draft


# ---------------------------------------------------------
# 2) REPLY DRAFT USING threadId + messageId
# ---------------------------------------------------------
def create_reply_draft(thread_id, recipient, subject, body, message_id=None):
    """
    Create a draft reply inside the same Gmail thread.
    If message_id is given, adds proper reply headers.
    """
    service = get_service()

    message = MIMEText(body, "plain")
    message["to"] = recipient
    message["subject"] = subject

    # These headers ensure Gmail treats it as a reply
    if message_id:
        message["In-Reply-To"] = message_id
        message["References"] = message_id

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode("utf-8")

    draft_body = {
        "message": {
            "raw": encoded_message,
            "threadId": thread_id
        }
    }

    draft = service.users().drafts().create(
        userId="me",
        body=draft_body
    ).execute()

    print("Reply draft created successfully!")
    return draft


# ---------------------------------------------------------
# TESTING AREA
# ---------------------------------------------------------
# if __name__ == "__main__":

#     print("\n1️⃣ Creating normal draft...")
#     # create_draft(
#     #     thread_id="19b0e6bebcb7d181",
#     #     recipient="preetnandeshwar8@gmail.com",
#     #     subject="Looking for job",
#     #     body="I finally got job in Accenture"
#     # )

#     create_reply_draft(
#     thread_id="19b0e6bebcb7d181",
#     recipient="preetnandeshwar8@gmail.com",
#     subject="Re: Looking for job",
#     body="I finally got job in Accenture",
#     message_id = "19b0e6bebcb7d181")


#     # Example for reply draft (use your real threadId and messageId)
#     # print("\n2️⃣ Creating reply draft...")
#     # create_reply_draft(
#     #     thread_id="YOUR_THREAD_ID",
#     #     recipient="someone@example.com",
#     #     subject="Re: Example subject",
#     #     body="This is my reply message",
#     #     message_id="<MESSAGE_ID_FROM_EMAIL>"
#     # )
