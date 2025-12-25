import streamlit as st
import os
from graph import create_graph # Import the function, not the object

# --- 1. Page Config ---
st.set_page_config(page_title="Deep Research Agent", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ Deep Research Assistant")

# --- 2. Sidebar: API Keys & Sources ---
with st.sidebar:
    st.header("🔑 API Configuration")
    st.info("Enter your API keys to activate the agent.")
    
    # Input fields for keys
    google_api_key = st.text_input("Google API Key", type="password", help="Get it from Google AI Studio")
    tavily_api_key = st.text_input("Tavily API Key", type="password", help="Get it from tavily.com")
    
    st.divider()
    
    # Source Inspector (Only shows up if we have sources)
    st.header("📚 Referenced Sources")
    if "last_sources" in st.session_state and st.session_state.last_sources:
        for source in st.session_state.last_sources:
            with st.expander(f"Source: {source['url'][:30]}..."):
                st.write(source['content'])
                st.markdown(f"[Visit Link]({source['url']})")

# --- 3. Session State & Key Verification ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Check if keys are provided
if not google_api_key or not tavily_api_key:
    st.warning("⚠️ Please enter both API keys in the sidebar to proceed.")
    st.stop() # Stop execution here until keys are entered

# Set environment variables dynamically
os.environ["GOOGLE_API_KEY"] = google_api_key
os.environ["TAVILY_API_KEY"] = tavily_api_key

# Initialize Graph (Cached to avoid rebuilding on every rerun)
if "graph" not in st.session_state:
    st.session_state.graph = create_graph()

# --- 4. Chat Interface ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a research question..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("🕵️‍♂️ Researching..."):
        try:
            # Run the graph
            response = st.session_state.graph.invoke({"question": prompt})
            final_answer = response["answer"]
            
            # Save sources
            raw_context = response.get("context", [])
            parsed_sources = []
            for item in raw_context:
                lines = item.split("\n")
                url = lines[1].replace("URL: ", "").strip() if len(lines) > 1 else "Unknown"
                parsed_sources.append({"url": url, "content": item})
            
            st.session_state.last_sources = parsed_sources

            # Show Answer
            with st.chat_message("assistant"):
                st.markdown(final_answer)
            st.session_state.messages.append({"role": "assistant", "content": final_answer})
            
            # Refresh to show sources in sidebar
            st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred: {e}")