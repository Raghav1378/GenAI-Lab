import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI
from langserve import add_routes
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import Runnable
import uvicorn

# Load environment variables
load_dotenv()

# ---------- Custom Hugging Face Wrapper ----------
class HuggingFaceChatModel(Runnable):
    """
    Simple invoke-based Hugging Face chat model using OpenAI-compatible API.
    Works standalone or inside LangChain pipelines.
    """

    def __init__(self, model_name="openai/gpt-oss-20b", api_key=None):
        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=api_key or os.getenv("HF_TOKEN"),
        )
        self.model_name = model_name

    def invoke(self, input, config=None):
        """
        LangChain-compatible invoke method.
        Accepts a dict with 'text' key or a plain string.
        """
        if isinstance(input, dict):
            prompt = input.get("text", "")
        else:
            prompt = str(input)

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty or whitespace.")

        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"[Error] {e}"

# ---------- Model Instances ----------
huggingface_model = HuggingFaceChatModel(model_name="openai/gpt-oss-20b")
gemini_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# ---------- Common Chain Components ----------
parser = StrOutputParser()

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", "{text}")
])

# ---------- Define Two Chains ----------
hf_chain = prompt_template | huggingface_model | parser
gemini_chain = prompt_template | gemini_model | parser

# ---------- FastAPI Setup ----------
app = FastAPI(
    title="SimpleTranslator",
    version="1.0",
    description="A simple API server using LangChain Runnables for translation with Gemini & HuggingFace",
)

# ---------- Add Routes ----------
add_routes(app, hf_chain, path="/translate-hf")
add_routes(app, gemini_chain, path="/translate-gemini")

# ---------- Run Server ----------
if __name__ == "__main__":
    print("✅ Server running on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
