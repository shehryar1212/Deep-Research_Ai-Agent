#  Deep Research AI Agent

> **An autonomous, self-correcting multi-agent system that performs deep web research, verifies facts, and writes professional reports.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://deep-researchai-agent-xbjzswvylnjfgvqwxevky4.streamlit.app/)
![Python 3.11](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange)
![Tavily API](https://img.shields.io/badge/Search-Tavily_API-green)

---

##  The Problem
Standard chatbots (like ChatGPT) often hallucinate or provide surface-level answers. They lack the ability to **"stop and check their work."**

##  The Solution: Agentic AI
This project builds a **Virtual Research Team** where multiple AI agents collaborate in a loop. It treats the LLM not just as a text generator, but as a **reasoning engine** that orchestrates a specific workflow.

### 👥 The "Squad"
1.   The Researcher: Uses the **Tavily Search API** to scour the web for real-time, cited information.
2.   The Editor (The Critic): Evaluates the Researcher's notes for relevance and accuracy. If the data is insufficient, it **rejects** the findings and sends the Researcher back to work (Self-Correction Loop).
3.   The Writer: Compiles the approved, verified facts into a structured final report.

---

## 🧠 Architecture (State Machine)

The system is built using **LangGraph**, creating a cyclical graph where state is passed between nodes.

```mermaid
graph TD
    Start([User Topic]) --> Researcher
    Researcher[ Researcher Node] -->|Web Search Results| Editor
    Editor[ Editor Node] -->|Review & Critique| Decision{Is Data Sufficient?}
    
    Decision -- "❌ No (Reject)" --> Researcher
    Decision -- "✅ Yes (Approve)" --> Writer
    
    Writer[ Writer Node] --> End([Final Report])
    
    style Decision fill:#f9f,stroke:#333,stroke-width:2px
    style Researcher fill:#bbf,stroke:#333
    style Editor fill:#dfd,stroke:#333
