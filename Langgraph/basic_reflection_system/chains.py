from dotenv import load_dotenv
import os

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# ---------------------------------------cd------------------
#  FIXED MODEL (now uses API key properly)
# ---------------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# ---------------------------------------------------------
#  GENERATION PROMPT (fixed broken system message!)
# ---------------------------------------------------------
generation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "You are a tech influencer assistant tasked with writing "
            "viral, high-quality Twitter posts.\n"
            "Generate the best tweet possible for the user's request.\n"
            "If the user provides critique, rewrite and improve the tweet.\n"
        )
    ),
    MessagesPlaceholder(variable_name="messages")
])

# ---------------------------------------------------------
#  REFLECTION PROMPT
# ---------------------------------------------------------
reflection_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "You are a viral Twitter influencer.\n"
            "Your job is to critique the tweet and suggest improvements.\n"
            "Always provide detailed notes on virality, clarity, style, and structure."
        ),
    ),
    MessagesPlaceholder(variable_name="messages"),
])

# ---------------------------------------------------------
# FIXED CHAINS
# ---------------------------------------------------------
generation_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm
