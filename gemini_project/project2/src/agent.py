import os
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from dotenv import load_dotenv

load_dotenv()

def get_agent(df):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_output_tokens=None,
        timeout=None,
    )

    # We add a specific instruction (prefix) to guide the agent
    instruction = """
    You are a data expert. 
    When asked to plot or visualize:
    1. Use 'matplotlib' or 'seaborn'.
    2. ALWAYS save the plot to a file named 'plot.png'.
    3. DO NOT use plt.show().
    4. Return the answer "I have saved the plot." after saving.
    """

    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True,
        agent_type="openai-tools",
        prefix=instruction, # <--- This inserts our rule
    )
    return agent

def analyze_data(agent, query):
    try:
        response = agent.invoke(query)
        output = response.get('output')

        # Clean up the response (remove JSON artifacts)
        if isinstance(output, list):
            final_text = ""
            for item in output:
                if isinstance(item, dict) and 'text' in item:
                    final_text += item['text']
            return final_text
        
        return str(output)

    except Exception as e:
        return f"Error analyzing data: {str(e)}"