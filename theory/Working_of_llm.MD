genai_mastery:
  day: 1
  topic: "How LLMs Actually Work — End-to-End Theory (Beginner → Engineer Level)"
  sections:

    - heading: "1. What is an LLM?"
      content: |
        A Large Language Model (LLM) is a pattern prediction machine.
        It is trained to guess the most probable next token (word/piece of word)
        based on the text it has already seen.

        Example:
          Prompt: "Raghav went to the store to buy a"
          Model prediction probabilities:
            - mango: 0.41
            - pen:   0.29
            - phone: 0.09
        
        It selects the most likely next token.
        LLMs do NOT think — they predict using patterns learned from huge datasets.

    - heading: "2. Tokenization — Breaking Text Into Pieces"
      content: |
        LLMs cannot read words directly.
        All input is broken into tiny chunks called 'tokens'.

        Example:
          "Raghav loves samosa" becomes:
            ["Rag", "hav", "love", "samo", "sa"]

        Each token is then mapped to a numeric ID.
        Tokenization ensures the model can process any language.

    - heading: "3. Embeddings — Giving Meaning to Tokens"
      content: |
        Every token ID is converted into a 'vector' (a list of numbers).
        This vector captures the meaning of that token.

        Example:
          doctor → [0.12, -0.44, 0.93, ...]
          nurse  → [0.11, -0.46, 0.91, ...]

        The closer the vectors, the more similar the meanings.

    - heading: "4. Transformer Architecture — The Engine Inside LLMs"
      content: |
        Transformers process tokens using stacked layers (12–96+).
        Each layer transforms the token embeddings into deeper meaning.

        Key components per layer:
          - Multi-Head Self-Attention
          - Feed-Forward Neural Network
          - Layer Normalization
          - Residual Connections

        Transformers allow LLMs to consider entire context, not just nearby words.

    - heading: "5. Self-Attention — The Brain of an LLM"
      content: |
        Self-attention allows the model to figure out:
          "Which words in the sentence are relevant to each other?"

        Example:
          "Raghav gave his pen to Arun because he needed it."

        To understand "he":
          - Look at "Arun"
          - Look at "Raghav"
          - Look at context
        
        Self-attention assigns weights:
          he → Arun   (0.78)
          he → Raghav (0.22)
          he → pen    (0.00)

        This enables LLMs to understand relationships and context.

    - heading: "6. Multi-Head Attention — Multiple Perspectives at Once"
      content: |
        Instead of one attention map, the model creates many attention heads.
        Each head learns a different pattern:
          - grammar head
          - reference head
          - semantic meaning head
          - position head
          - intent head

        Multiple heads = richer understanding.

    - heading: "7. Feed-Forward Processing"
      content: |
        After attention, each token embedding passes through a small neural network
        (inside each transformer layer).
        
        This adds:
          - abstraction
          - non-linearity
          - deeper representation

    - heading: "8. Layer Stacking — Building Understanding Step-by-Step"
      content: |
        Transformers have many layers.
        Each layer refines the understanding of the input.

        Layer 1: basic meaning  
        Layer 12: contextual meaning  
        Layer 48: deep reasoning, long context relationships  

        By the final layer, the model has a strong representation of the entire prompt.

    - heading: "9. Softmax — Predicting the Next Token"
      content: |
        After passing through all layers, the model outputs a probability
        distribution for the next token.

        Example:
          mango: 0.41
          apple: 0.38
          water: 0.02

        It picks the token with the highest probability, adds it to output,
        and repeats.

    - heading: "10. Why LLMs Feel Intelligent"
      content: |
        Because language itself has patterns, structure, logic, emotion,
        tone, and relationships, predicting the next token accurately
        can FEEL like "thinking".

        But fundamentally, LLMs are pattern machines trained on billions
        of sentences. Great prediction = illusion of intelligence.

    - heading: "11. Why This Matters"
      content: |
        Understanding LLM mechanics explains all advanced GenAI topics:

          - RAG:    External knowledge because LLMs cannot store everything.
          - Agents: Tools and planning because LLMs cannot act alone.
          - LangGraph: Structure and control to prevent hallucination.
          - LangSmith: Monitoring the internal reasoning process.
          - Fine-Tuning: Modifying the behavior of the prediction engine.
          - Embeddings: Vector search is the same embedding concept reused.

        Everything in GenAI sits on top of this foundation.

    - heading: "12. Easy Real-Life Analogy"
      content: |
        Think of an LLM like a student who:
          - read 1 billion books
          - remembers patterns
          - sees your sentence
          - predicts what probably comes next
          - uses attention to decide which words matter
          - sometimes makes confident mistakes
          - can be guided with instructions
          - can be extended using notes (RAG)
          - can be given tools (Agents)
          - can be controlled using workflow (LangGraph)
          - can be monitored using CCTV (LangSmith)

        No magic. Just massive pattern learning and smart structure.

  next_day_topic: "Day 2 — Deep Dive: Self-Attention (Q/K/V, Matrices, Heads, Math)"
