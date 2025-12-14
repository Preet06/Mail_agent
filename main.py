from fastapi import FastAPI
from pydantic import BaseModel
# from agent_ai import ask_agent
# from gmail_read_write.math import agent,model_client
import logging
from autogen_agentchat.ui import Console
from autogen_agentchat.agents import AssistantAgent

from gmail_read_write.gmail_write import create_reply_draft
logging.basicConfig(level=logging.INFO)
import autogen
from typing import Annotated
import json
import logging
from fastapi import FastAPI
from pydantic import BaseModel
import autogen
import asyncio
from typing import Annotated
# from agent_framework import ChatMessage
from agent_framework.openai import OpenAIChatClient

# ====================================
# PUT YOUR GEMINI API KEY HERE
# ====================================
API_KEY = "AIzaSyBTwHw9fCN3RjDRt7RissQuwpJE95jsw7s"


# ====================================
# FASTAPI APP
# ====================================
app = FastAPI()

# ====================================
# AUTOGEN AGENT CONFIG
# ====================================
config_list = [
    {
        "model": "gemini-2.5-flash",
        "api_key": API_KEY,
        "api_type": "google"
    }
]

client = OpenAIChatClient(
    model_id="gemini-2.5-flash",
    api_key="AIzaSyB_BPRbu-pvrNR7BwfcCyTMS-clpc9g6aE",
    base_url="https://generativelanguage.googleapis.com/v1beta/"  # Google's endpoint
)


# ====================================
# LOAD EMAIL JSON FILE
# ====================================
with open("gmail_read_write/email_data.json", "r", encoding="utf-8") as f:
    EMAIL_DATA = json.load(f)

agent = client.create_agent(
        instructions="Does the email need reply? if yes then return the appropriate reply." \
    " This info ,ight be useful for reply. Current CTC is 5.6, Expected CTC is 12 LPA. Fill information which you have otherwise just mention NANA." \
    " If email don't need reply then just return No"
    )

async def main():
    for email in EMAIL_DATA:
        email_body = email.get("body", "")

        response = await agent.run(email_body)
        print("Agent raw response:", response)

        # ✅ Convert agent response to plain text
        reply_text = response.content if hasattr(response, "content") else str(response)

        if reply_text.strip() != "No":
            create_reply_draft(
                thread_id=email.get("threadId"),
                recipient=email.get("sender"),
                subject=f"Re: {email.get('subject')}",
                body=reply_text,          # ✅ STRING ONLY
                message_id=email.get("messageId")
            )


asyncio.run(main())



# if __name__ == "__main__":
#     assistant.run("SALE SALE SALE")


