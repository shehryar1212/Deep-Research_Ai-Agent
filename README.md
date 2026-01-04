#  Deep Research AI Agent

> **An autonomous multi-agent system that iteratively researches, critiques, and writes professional reports on any topic.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://deep-researchai-agent-xbjzswvylnjfgvqwxevky4.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangGraph](https://img.shields.io/badge/AI-LangGraph-orange)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)

---

##  Overview

This isn't just a chatbot. It is a **Self-Correcting State Machine**.

When you give this agent a topic, it spawns a virtual team of AI employees:
1.  ** Researcher:** Uses **Tavily Search API** to scour the web for real-time facts.
2.  ** Editor:** Reviews the findings. If the data is weak or irrelevant, it **rejects** the work and sends the Researcher back to the web (Looping Mechanism).
3.  ** Writer:** Once the Editor approves, the Writer compiles the facts into a polished, comprehensive report.

Built with **LangGraph** for state management and **Streamlit** for the frontend interface.

---

## ⚙️ Architecture

The system uses a cyclical graph workflow to ensure quality control:

```mermaid
graph TD
    Start([User Request]) --> Researcher
    Researcher[ Researcher] -->|Web Search| Editor
    Editor[ Editor] -->|Decision| Router{Is Data Good?}
    Router -- "❌ No (Reject)" --> Researcher
    Router -- "✅ Yes (Approve)" --> Writer
    Writer[ Writer] --> End([Final Report])
