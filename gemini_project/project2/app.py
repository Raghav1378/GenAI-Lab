import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from src.agent import get_agent, analyze_data

# 1. Load Environment Variables
load_dotenv()

# 2. Page Configuration
st.set_page_config(
    page_title="Data Analyst Agent",
    page_icon="📊",
    layout="wide"
)

# 3. Custom CSS for better styling
st.markdown("""
    <style>
    .stChatFloatingInputContainer {bottom: 20px;}
    .main {background-color: #f9f9f9;}
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar: File Upload
with st.sidebar:
    st.header("📂 Data Source")
    st.write("Upload a CSV file to start analyzing.")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        if os.path.exists("plot.png"):
            os.remove("plot.png")
        st.rerun()

# 5. Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Main App Logic
st.title("🤖 AI Data Analyst")
st.write("Ask questions about your data, get insights, and see the code.")

if uploaded_file is not None:
    try:
        # Load and Cache Data
        if "df" not in st.session_state or st.session_state.get("uploaded_file_name") != uploaded_file.name:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.session_state.uploaded_file_name = uploaded_file.name
            st.success(f"Loaded {uploaded_file.name} successfully! ({len(st.session_state.df)} rows)")
        
        df = st.session_state.df

        # Preview Data
        with st.expander("👀 Preview Data"):
            st.dataframe(df.head())

        # Initialize Agent
        agent = get_agent(df)

        # Display Chat History
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                # Note: We cannot easily re-display old images from history in this simple version 
                # because we delete the file. For a persistent history, we'd need to save unique filenames.

        # Handle User Input
        if prompt := st.chat_input("Ex: 'Show me the sales trend for Q3' or 'Plot Sales by Region'"):
            
            # A. Display User Message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # B. Generate Assistant Response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing data..."):
                    
                    # 1. Run the Agent Logic
                    response = analyze_data(agent, prompt)
                    st.markdown(response)
                    
                    # 2. Check for and Display Plot
                    # The agent in agent.py is instructed to save plots as 'plot.png'
                    if os.path.exists("plot.png"):
                        st.image("plot.png", caption="Generated Visualization")
                        
                        # (Optional) Clean up to prevent showing stale charts later
                        # If you want to keep it in history, you'd need to rename it with a timestamp
                        os.remove("plot.png") 

            # C. Save Text Response to History
            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("👈 Please upload a CSV file in the sidebar to begin.")