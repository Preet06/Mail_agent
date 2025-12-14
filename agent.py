# """
# Simple AutoGen Agent with Gemini - Math Calculator
# ===================================================
# Before running this code:
# 1. Install required packages (IMPORTANT - RUN THIS):
#    pip install ag2[gemini]

# 2. Get your Gemini API key:
#    - Go to https://makersuite.google.com/app/apikey
#    - Create a new API key
#    - Copy it and paste it in the API_KEY variable below
# """

# import autogen
# from typing import Annotated
# from typing import Annotated
# from agent_framework import ChatAgent, Tool
# from agent_framework.openai import OpenAIChatClient
# # ====================================
# # PUT YOUR GEMINI API KEY HERE
# # ====================================
# API_KEY = "AIzaSyBTwHw9fCN3RjDRt7RissQuwpJE95jsw7s"

# # ====================================
# # DEFINE THE 4 MATH FUNCTIONS
# # ====================================

# from agent_framework import ChatAgent
# from agent_framework.openai import OpenAIChatClient


# # def add_numbers(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
# #     """Add two numbers together"""
# #     result = a + b
# #     print(f"Adding: {a} + {b} = {result}")
# #     return result

# # def subtract_numbers(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
# #     """Subtract second number from first number"""
# #     result = a - b
# #     print(f"Subtracting: {a} - {b} = {result}")
# #     return result

# # def multiply_numbers(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
# #     """Multiply two numbers together"""
# #     result = a * b
# #     print(f"Multiplying: {a} × {b} = {result}")
# #     return result

# # def divide_numbers(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
# #     """Divide first number by second number"""
# #     if b == 0:
# #         return "Error: Cannot divide by zero!"
# #     result = a / b
# #     print(f"Dividing: {a} ÷ {b} = {result}")
# #     return result





# # Configure the Gemini model
# config_list = [
#     {
#         "model": "gemini-2.5-flash",
#         "api_key": API_KEY,
#         "api_type": "google"
#     }
# ]



# client = OpenAIChatClient(
#     model_id="gemini-2.5-flash",
#     api_key="AIzaSyBTwHw9fCN3RjDRt7RissQuwpJE95jsw7s",
#     api_type="google"
# )

# agent = ChatAgent(
#     chat_client=client,
#     instructions="You are a helpful assistant.",
#     name="OpenAI Assistant"
# )





# # # Create the assistant agent (this is the AI that does the math)
# # assistant = autogen.AssistantAgent(
# #     name="MathAssistant",
# #     llm_config={
# #         "config_list": config_list,
# #         "temperature": 0,
# #     },
# #     system_message="""You are a helpful math assistant with access to calculator functions.
# #     When a user asks you to perform math operations, use the appropriate function.
# #     Always call the correct function based on what the user asks."""
# # )

# # # Create the user proxy agent with function execution enabled
# # user_proxy = autogen.UserProxyAgent(
# #     name="User",
# #     human_input_mode="NEVER",
# #     max_consecutive_auto_reply=3,  # Stop after one response
# #     # is_termination_msg=lambda x: True,
# #     code_execution_config=False,
# # )

# # # Register all 4 functions with both agents
# # autogen.register_function(
# #     add_numbers,
# #     caller=assistant,
# #     executor=user_proxy,
# #     name="add_numbers",
# #     description="Add two numbers together"
# # )

# # autogen.register_function(
# #     subtract_numbers,
# #     caller=assistant,
# #     executor=user_proxy,
# #     name="subtract_numbers",
# #     description="Subtract second number from first number"
# # )

# # autogen.register_function(
# #     multiply_numbers,
# #     caller=assistant,
# #     executor=user_proxy,
# #     name="multiply_numbers",
# #     description="Multiply two numbers together"
# # )

# # autogen.register_function(
# #     divide_numbers,
# #     caller=assistant,
# #     executor=user_proxy,
# #     name="divide_numbers",
# #     description="Divide first number by second number"
# # )

# # ====================================
# # MAIN PROGRAM - CHANGE YOUR QUERY HERE
# # ====================================
# # if __name__ == "__main__":
# #     print("Starting AutoGen Math Calculator Agent...")
# #     print("=" * 60)
    
# #     # ====================================
# #     # CHANGE YOUR QUERY HERE
# #     # ====================================
# #     # Examples you can try:
# #     # "Add 25 and 37"
# #     # "Subtract 10 from 50"
# #     # "Multiply 7 and 8"
# #     # "Divide 100 by 4"
# #     # "What is 15 plus 25?"
# #     # "Calculate 20 times 5"
    
# #     query = "muliply 25 and 1 and then Add 5 in it"  # Change this to your instruction
    
# #     print(f"Your Query: {query}")
# #     print("=" * 60)
    
# #     # Start the conversation
# #     user_proxy.initiate_chat(
# #         assistant,
# #         message=query
# #     )
    
# #     print("=" * 60)
# #     print("Done!")

# # ====================================
# # HOW TO USE THIS CODE:
# # ====================================
# # 1. Replace "your-gemini-api-key-here" with your actual Gemini API key
# # 2. Change the 'query' variable to ask for any math operation
# # 3. Run: python agent.py
# # 4. The AI will understand your query and call the right function!
# #
# # Example queries you can try:
# # - "Add 100 and 200"
# # - "What is 50 minus 30?"
# # - "Multiply 12 by 8"
# # - "Divide 144 by 12"
# # - "Calculate 25 plus 75"
# # - "What's 200 divided by 5?"




































import asyncio
from typing import Annotated
# from agent_framework import ChatMessage
from agent_framework.openai import OpenAIChatClient
# Math functions
def add_numbers(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    return a + b

def subtract_numbers(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    return a - b

def multiply_numbers(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    return a * b

def divide_numbers(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    if b == 0:
        return "Error: Cannot divide by zero!"
    return a / b

email_data="You are e,ail analyser. and this is the email -"

# Client (OpenAI only)
client = OpenAIChatClient(
    model_id="gemini-2.5-flash",
    api_key="AIzaSyB_BPRbu-pvrNR7BwfcCyTMS-clpc9g6aE",
    base_url="https://generativelanguage.googleapis.com/v1beta/"  # Google's endpoint
)

# Agent
agent = client.create_agent(
    instructions=email_data,
    tools=[add_numbers, subtract_numbers, multiply_numbers, divide_numbers]
)

# Async test
async def main():
    response = await agent.run("Does the email need reply? if yes then return the appropriate reply." \
    " This info ,ight be useful for reply. Current CTC is 5.6, Expected CTC is 12 LPA. Fill information which you have otherwise just mention NANA." \
    " If email don't need reply then just return No")
    print("Agent response:", response.text)

asyncio.run(main())
