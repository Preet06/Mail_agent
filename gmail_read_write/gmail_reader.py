from __future__ import print_function
import os
import json
import base64

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_service():
    """Authenticate and return Gmail service."""
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def extract_body(payload):
    """Extract plain text or HTML email body."""
    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")
            if mime_type in ["text/plain", "text/html"]:
                data = part["body"].get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8")
    else:
        data = payload["body"].get("data")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8")
    return ""


def get_unread_emails():
    """Fetch all unread emails with complete important fields."""
    service = get_service()

    results = service.users().messages().list(
        userId="me",
        q="is:unread"
    ).execute()

    messages = results.get("messages", [])
    email_list = []

    print(f"Found {len(messages)} unread emails")

    for msg in messages:
        msg_detail = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        payload = msg_detail.get("payload", {})
        headers = payload.get("headers", [])

        subject = sender = receiver = ""

        # Extract useful header values
        for h in headers:
            name = h.get("name")
            value = h.get("value", "")
            if name == "Subject":
                subject = value
            elif name == "From":
                sender = value
            elif name == "To":
                receiver = value

        body = extract_body(payload)
        snippet = msg_detail.get("snippet", "")

        # Build JSON with all required fields
        email_json = {
            "id": msg["id"],
            "messageId": msg_detail.get("id"),
            "threadId": msg_detail.get("threadId"),
            "subject": subject,
            "sender": sender,
            "receiver": receiver,
            "snippet": snippet,
            "body": body
        }

        email_list.append(email_json)

    return email_list


def save_to_file(data, filename="email_data.json"):
    """Overwrite the old file with fresh email data."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Saved {len(data)} emails to {filename}")


if __name__ == "__main__":
    unread_messages = get_unread_emails()
    save_to_file(unread_messages)
