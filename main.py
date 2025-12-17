from __future__ import print_function

# ==============================
# STANDARD IMPORTS
# ==============================
import json
import asyncio
import logging
from fastapi import FastAPI

# ==============================
# GMAIL MODULE IMPORTS
# ==============================
from gmail_read_write.gmail_reader import get_unread_emails, save_to_file
from gmail_read_write.gmail_write import create_reply_draft

# ==============================
# AUTOGEN / AGENT IMPORTS
# ==============================
from agent_framework.openai import OpenAIChatClient

# ==============================
# LOGGING
# ==============================
logging.basicConfig(level=logging.INFO)

# ==============================
# FASTAPI APP (OPTIONAL FUTURE USE)
# ==============================
app = FastAPI()

# ==============================
# API CONFIG
# ==============================
API_KEY = "YOUR_GEMINI_API_KEY"

client = OpenAIChatClient(
    model_id="gemini-2.5-flash",
    api_key="AIzaSyD-lfNCXdikYjE-0mSNQF1gFjbI9KKdvXs",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# ==============================
# CREATE AGENT
# ==============================
agent = client.create_agent(
    instructions=(
        "Role:\n"
        "You are an expert Talent Acquisition Assistant.\n\n"

        "Objective:\n"
        "Analyze incoming candidate emails and decide whether a reply is required. "
        "If a reply is required, generate a clear, professional response.\n\n"

        "Inputs Provided:\n"
        "1. Email Content\n"
        "2. Candidate Details\n\n"

        "Decision Rules:\n"
        "- Reply YES if the email:\n"
        "  • Contains a question\n"
        "  • Requests information\n"
        "  • Invites discussion, interview, or call\n"
        "  • Asks about salary, notice period, experience, or availability\n\n"
        "- Reply NO if the email:\n"
        "  • Is only an acknowledgment\n"
        "  • Is a simple thank-you without questions\n"
        "  • Is a generic notification or system message\n\n"

        "Response Rules:\n"
        "- If NO reply is required, return exactly:\n"
        "  No\n\n"
        "- If YES, write a concise, polite, and professional reply.\n"
        "- Use ONLY the provided Candidate Details.\n"
        "- If any requested information is missing, use the placeholder NA.\n"
        "- Do NOT invent or assume any information.\n\n"

        "Candidate Details:\n"
        "- Current CTC: 6.5 LPA\n"
        "- Expected CTC: 10 LPA\n"
        "- Notice Period: 30 Days\n"
        "- Current Location: Nagpur\n"
        "- Preferred Location: Pan India\n"
        "- Experience (GenAI): 1.5 Years\n"
        "- Experience (Python): 1.5 Years\n"
        "- Experience (LLM-RAG): 1.5 Years\n"
        "- Experience (Cloud): 2 Years\n"
    )
)


# ==============================
# MAIN ASYNC LOGIC
# ==============================
async def process_emails():
    print("📥 Fetching unread emails...")

    unread_messages = get_unread_emails()
    save_to_file(unread_messages)

    if not unread_messages:
        print("✅ No unread emails. Exiting.")
        return

    print(f"📧 Processing {len(unread_messages)} emails with AI...")

    with open("email_data.json", "r", encoding="utf-8") as f:
        email_data = json.load(f)

    for email in email_data:
        email_body = email.get("body", "")

        response = await agent.run(email_body)

        reply_text = (
            response.content
            if hasattr(response, "content")
            else str(response)
        )

        print("\n🤖 Agent Response:\n", reply_text)

        if reply_text.strip() != "No":
            create_reply_draft(
                thread_id=email.get("threadId"),
                recipient=email.get("sender"),
                subject=f"Re: {email.get('subject')}",
                body=reply_text,
                message_id=email.get("messageId")  # MUST be Message-ID header
            )

            print("✉️ Draft reply created")

# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    asyncio.run(process_emails())
