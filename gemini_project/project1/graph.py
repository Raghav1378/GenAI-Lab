from typing import TypedDict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END

# --- Define the State ---
class AgentState(TypedDict):
    question: str
    context: List[str]
    answer: str

def create_graph():
    """
    Initializes the graph, tools, and LLM only when called.
    This ensures we don't crash if API keys are missing at import time.
    """
    
    # --- Initialize Tools & Model ---
    # These will automatically look for keys in os.environ which we set in app.py
    search_tool = TavilySearchResults(max_results=3)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    # --- Define Nodes ---
    def search_node(state: AgentState):
        query = state["question"]
        results = search_tool.invoke({"query": query})
        
        formatted_context = []
        for i, result in enumerate(results):
            content = f"Source ID [{i+1}]:\nURL: {result['url']}\nContent: {result['content']}\n"
            formatted_context.append(content)
            
        return {"context": formatted_context}

    def generate_node(state: AgentState):
        question = state["question"]
        context_block = "\n---\n".join(state["context"])
        
        prompt = f"""
        You are a smart research assistant. Use the provided Context to answer the user.

        User Question: {question}

        Search Results (Context):
        {context_block}

        Instructions:
        1. Answer clearly and concisely.
        2. STRICT CITATION RULE: You must cite your sources using the Source IDs provided (e.g., [1], [2]).
        3. If the answer is not in the context, state that you couldn't find specific information.
        """
        
        response = llm.invoke(prompt)
        return {"answer": response.content}

    # --- Build Graph ---
    workflow = StateGraph(AgentState)
    workflow.add_node("researcher", search_node)
    workflow.add_node("writer", generate_node)
    
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", END)
    
    return workflow.compile()