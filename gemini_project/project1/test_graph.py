from graph import graph

# Test query
query = "What are the latest features of Python 3.13?"

print(f"🚀 Starting run for: {query}")

# Run the graph
result = graph.invoke({"question": query})

print("\n--- FINAL ANSWER ---\n")
print(result["answer"])