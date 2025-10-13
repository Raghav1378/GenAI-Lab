# Working of RAG (Retrieval-Augmented Generation)

This document explains **step-by-step how RAG works**, from receiving a query to generating a final answer.

---

## 1. User Query

- The process starts when a **user inputs a question** or prompt.
- Example:  
  `"What are the side effects of Drug X?"`

---

## 2. Document Retrieval

- The **Retriever** searches a knowledge base or dataset for relevant documents.
- Retrieval methods:
  - **Sparse retrieval**: TF-IDF, BM25
  - **Dense retrieval**: Embeddings + similarity search
- Output: **Top-k relevant documents** for the query.

**Example:**

- Query: `"RAG in AI"`
- Retriever fetches 5 most relevant documents explaining RAG concepts.

---

## 3. Context Construction

- The retrieved documents are **combined with the query** to form the input for the generator.
- This step ensures the model has:
  - Contextual information
  - Factual references
  - Updated knowledge

**Key Point:** This allows the LLM to avoid hallucinations and produce accurate answers.

---

## 4. Answer Generation

- The **Generator** (LLM) uses the query + retrieved context to generate the response.
- Approaches:
  - **RAG-Sequence**: Generates answer token by token using all retrieved documents.
  - **RAG-Token**: Considers each token from the retrieved docs probabilistically.

**Result:** A coherent, context-aware response.

---

## 5. Output

- The final **answer is returned** to the user.
- Example:  
  `"Drug X may cause nausea, dizziness, and mild headaches. Refer to official medical guidelines for detailed information."`

---

## 6. Summary Flow (Stepwise)

1. **Input:** User asks a question.
2. **Retrieve:** Fetch top-k relevant documents from knowledge base.
3. **Combine:** Merge query + retrieved documents.
4. **Generate:** LLM creates an answer using combined context.
5. **Output:** Present accurate, contextual response to user.

---

## 7. Diagram

User Query → Retriever → Top-k Docs → Context Construction → Generator (LLM) → Output
