# 🕵️‍♂️ Deep Research AI Agent

**An autonomous research assistant that browses the web, synthesizes data, and provides answers with inline citations.**

![App Screenshot](assets/screenshot.png) 
*(Note: Take a screenshot of your app and put it in an 'assets' folder, or delete this line)*

## 🚀 Key Features
* **Multi-Step Reasoning:** Uses `LangGraph` to plan research steps rather than just answering blindly.
* **Live Web Access:** Integrated with **Tavily API** to fetch real-time data (not limited to training cutoff).
* **Hallucination Guardrails:** Enforces strict citation rules (`[1]`, `[2]`) linking back to source URLs.
* **Transparent UI:** Built with **Streamlit** to show the user exactly which sources were used in the sidebar.

## 🛠️ Tech Stack
* **Orchestration:** LangGraph & LangChain
* **LLM:** Google Gemini 1.5 Flash
* **Search Engine:** Tavily AI
* **Frontend:** Streamlit

## ⚙️ How it Works
1.  **User Query:** The user asks a complex question (e.g., "Compare Llama 3 vs GPT-4").
2.  **Researcher Node:** The agent identifies key search terms and queries the web.
3.  **Context Construction:** Search results are parsed and structured into a context block.
4.  **Writer Node:** The LLM generates an answer, citing the specific source IDs from the context.

## 📦 Setup & Installation
1.  Clone the repo:
    ```bash
    git clone [https://github.com/yourusername/research-agent.git](https://github.com/yourusername/research-agent.git)
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up environment variables in `.env`:
    ```text
    GOOGLE_API_KEY=your_key_here
    TAVILY_API_KEY=your_key_here
    ```
4.  Run the app:
    ```bash
    streamlit run app.py
    ```