# 🦜 LangChain Message Types: End-to-End Guide

In LangChain, "Messages" are the core units of communication between the user and the LLM. Each message type has a specific role in the conversation history.

Here is a breakdown of all main message types with code examples.

---

### 1. SystemMessage
**Role:** Sets the behavior, persona, or initial instructions for the AI. It is typically the first message sent in a sequence.
**Use Case:** Telling the AI "You are a helpful coding assistant" or "Answer only in JSON".

```python
from langchain_core.messages import SystemMessage

# Create a system message
sys_msg = SystemMessage(content="You are a sarcastic AI assistant that loves puns.")

print(sys_msg)
# Output: content='You are a sarcastic AI assistant that loves puns.'
```

---

### 2. HumanMessage
**Role:** Represents input from the user (you).
**Use Case:** The actual question or prompt sending to the model.

```python
from langchain_core.messages import HumanMessage

# Create a human message
human_msg = HumanMessage(content="Tell me a joke about Python.")

print(human_msg)
# Output: content='Tell me a joke about Python.'
```

---

### 3. AIMessage
**Role:** Represents the response back from the AI model.
**Use Case:** Storing the history of what the AI previously said or processing the model's output.

```python
from langchain_core.messages import AIMessage

# Create an AI message (simulating a response)
ai_msg = AIMessage(content="Why did the Python programmer need glasses? Because he couldn't C#!")

print(ai_msg)
# Output: content="Why did the Python programmer need glasses? Because he couldn't C#!"
```

---

### 4. ToolMessage (Modern)
**Role:** Represents the result of a tool execution.
**Use Case:** When an agent calls a tool (like a Google Search or Calculator), the output of that tool is passed back to the model as a `ToolMessage`.
**Note:** Critical for agents using OpenAI function calling or LangGraph.

```python
from langchain_core.messages import ToolMessage

# Simulate a tool output
tool_msg = ToolMessage(
    content="The current weather in New York is 72°F",
    tool_call_id="call_AbCd12345" # ID linking back to the AI's request to use the tool
)

print(tool_msg)
```

---

### 5. FunctionMessage (Legacy)
**Role:** Similar to `ToolMessage` but used in older OpenAI function calling implementations.
**Recommendation:** Use `ToolMessage` for newer projects.

```python
from langchain_core.messages import FunctionMessage

func_msg = FunctionMessage(
    content="{'result': 'success'}",
    name="get_weather"
)
```

---

### 6. ChatMessage (Generic)
**Role:** A customizable message type where you can manually specify the role.
**Use Case:** If you are using a model provider that supports roles other than system/user/ai (rare).

```python
from langchain_core.messages import ChatMessage

# Manually specifying a role
chat_msg = ChatMessage(
    role="observer", 
    content="I am watching the conversation."
)
```

---

### ⚡ Quick Summary for LangGraph/Chains
When building a standard chat history list for an LLM call, it usually looks like this:

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hi! I'm learning LangChain."),
    AIMessage(content="That's great! It's a powerful framework. What do you need help with?"),
    HumanMessage(content="Explain message types.")
]

# Pass 'messages' to your LLM
# llm.invoke(messages)
```
