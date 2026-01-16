# Recursive Language Model (RLM) Agent

An implementation of a **Recursive Language Model (RLM)** based on the research paper  
**_“Recursive Language Models” (Zhang et al., 2025)_**.

This project treats a large text prompt as an **external environment**, allowing an LLM to programmatically explore, decompose, and analyze data that exceeds its native context window.

---

## Overview

Traditional LLMs struggle with **context rot** or incur **high token costs** when processing extremely long documents.

This project implements a **Root–Sub architecture**:

- **Root LM (The Manager)**  
  Uses a high-reasoning model (`GPT-4o`) to plan, reason, and write Python code.

- **Environment (The REPL)**  
  A sandboxed Python execution environment where massive context is stored in **RAM**, not inside the LLM prompt.

- **Sub-LM (The Worker)**  
  A fast, cost-effective model (`GPT-4o-mini`) that the Root LM calls *recursively* to analyze specific text snippets.

---


## Features

- **Recursive Querying**  
  The Root LM can invoke `llm_query()` inside generated Python code to delegate semantic tasks to a Sub-LM.

- **Environment Isolation**  
  Large context is never fully sent to the API, saving thousands of tokens and avoiding context window limits.

- **Self-Correction**  
  The agent detects empty outputs or runtime errors and automatically retries with corrected logic  
  (e.g., fixing case-sensitivity or indexing issues).

- **Inference-Time Scaling**  
  Enables the model to “think longer” using programmatic tools, achieving higher accuracy on  
  **needle-in-a-haystack** and long-document reasoning tasks.

---

## Why Recursive Language Models?

RLMs decouple **reasoning** from **memory constraints**, enabling:

- Arbitrarily large document processing
- Tool-augmented and programmatic reasoning
- Cost-efficient task delegation
- Deterministic inspection and debugging

This architecture transforms the LLM from a passive text generator into an **active problem-solving agent**.


## Project Structure

```text
recursive-lm-project/
├── src/
│   ├── agent.py       # Orchestration logic (The Brain)
│   ├── repl.py        # Python execution environment (The Hands)
│   ├── llm_client.py  # Role-based API handling (Root vs. Sub)
│   └── prompts.py     # System instructions & RLM protocol
├── main.py            # Entry point & test simulation
├── .env               # API credentials (excluded via .gitignore)
├── .gitignore         # Protection for secrets and virtual environments
└── requirements.txt   # Project dependencies

