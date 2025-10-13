# End-to-End Working of RAG (Retrieval-Augmented Generation)

This document explains the **internal workflow of RAG**, from query input to final output, including splitting, retrieval, and generation steps.

---

## 1. Query Input

- A user provides a query or question.
- Example: `"Explain the side effects of Drug X."`
- This query is tokenized by the **RAG tokenizer** into input IDs that the model can process.

---

## 2. Query Embedding

- The tokenized query is passed to the **retriever encoder** to generate a **query embedding** (dense vector).
- Purpose: To represent the query numerically so it can be compared with document embeddings efficiently.

---

## 3. Document Retrieval

- RAG uses the query embedding to search a **document index** (knowledge base).
- Steps:
  1. **Split the documents** into smaller chunks (e.g., 100–500 tokens each) for efficient retrieval.
  2. Each chunk has its **precomputed embedding** stored in the index.
  3. Compute similarity between query embedding and document embeddings (e.g., cosine similarity).
  4. Retrieve **top-k most relevant document chunks**.

---

## 4. Context Construction

- The retrieved chunks are **combined with the original query** to form the context for generation.
- Two main strategies:
  - **Concatenation:** Join top-k documents + query as a single input sequence for the generator.
  - **Attention-based:** Model attends to each document separately while generating each token.

---

## 5. Generation

- The **generator (LLM)** uses the combined context to produce the answer.
- Two fusion approaches:

  - **RAG-Sequence:** Generates answer token by token conditioning on all retrieved documents.
    - Pros: Cohesive answers across multiple docs.
    - Cons: Slower for many documents.
  - **RAG-Token:** Generates each token by **marginalizing over all retrieved documents**.
    - Pros: Faster, can scale to many docs.
    - Cons: Slightly more complex, token-level fusion.

- During generation:
  1. The model predicts the next token based on the query + retrieved documents.
  2. Uses **beam search** or **greedy decoding** to construct the output sequence.
  3. Repeats until **end-of-sequence token** is produced.

---

## 6. Post-Processing

- Generated text is decoded from tokens back to readable text.
- Optional:
  - Remove irrelevant or duplicate info.
  - Apply formatting or clean-up for the user-facing output.

---

## 7. Output

- The final answer is returned to the user.
- Example:
  `"Drug X may cause nausea, dizziness, and mild headaches. Refer to official medical guidelines for details."`

---

## 8. Summary Flow (Stepwise)

1. **User Query:** Input from user.
2. **Tokenization:** Convert query into input IDs.
3. **Query Embedding:** Represent query as vector.
4. **Document Split & Retrieval:** Split corpus → compute similarities → fetch top-k chunks.
5. **Context Construction:** Combine query + retrieved docs.
6. **Generation:** LLM generates answer using sequence or token-level fusion.
7. **Post-Processing:** Clean or format output.
8. **Output:** Return final answer to user.

---

## 9. Diagram (Optional)

User Query → Tokenize → Embed → Split Docs → Retrieve Top-k → Combine Context → LLM Generation → Post-Processing → Output
