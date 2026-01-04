import operator
from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load keys first
load_dotenv()

# --- 1. The Shared State ---
class AgentState(TypedDict):
    task: str                
    research_data: List[str] 
    final_report: str        
    revision_count: int    
    review_status: str  
    messages: Annotated[List[BaseMessage], operator.add]

# --- 2. Setup Brain (DeepSeek via OpenRouter) ---
# We point the "base_url" to OpenRouter, but use the standard OpenAI class.
llm = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct:free", 
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0
)

# Setup Tool
search_tool = TavilySearchResults(max_results=3)


# --- 3. Node: The Researcher ---
def researcher_node(state: AgentState):
    print(" Researcher is searching...")
    query = state["task"]
    
    # If this is a retry (revision > 0), we append "more details" to the query
    if state.get("revision_count", 0) > 0:
        query += " detailed analysis statistics"

    try:
        results = search_tool.invoke(query)
        facts = [res["content"] for res in results]
    except Exception as e:
        facts = [f"Error: {str(e)}"]
    return {"research_data": facts}

# --- 5. Node: Editor (REAL LOGIC) ---
def editor_node(state: AgentState):
    print(" Editor is reviewing...")
    revision_count = state.get("revision_count", 0)
    research_data = state.get("research_data", [])

    # SAFETY VALVE: Stop infinite loops after 3 tries
    if revision_count >= 3:
        print("⚠️ Max revisions reached. Approving.")
        return {"review_status": "ACCEPT", "revision_count": revision_count}

    # Ask the AI to judge genuinely
    prompt = f"""
    You are a strict Editor. 
    User Task: {state['task']}
    
    Current Research Data: 
    {research_data}
    
    Analyze the data. Does it fully answer the User Task?
    - If the data is empty or irrelevant, say 'REJECT'.
    - If the data is good enough to write a report, say 'ACCEPT'.
    
    Only reply with 'ACCEPT' or 'REJECT'.
    """
    
    response = llm.invoke(prompt)
    decision = response.content.strip().upper()
    
    print(f" Editor Decision: {decision}")

    if "REJECT" in decision:
        return {"review_status": "REJECT", "revision_count": revision_count + 1}
    else:
        return {"review_status": "ACCEPT", "revision_count": revision_count}

# --- 6. Node: Writer ---
def writer_node(state: AgentState):
    print(" Writer is drafting...")
    facts = "\n\n".join(state["research_data"])
    prompt = f"""
    You are a professional journalist. Write a comprehensive report on: {state['task']}
    
    Use ONLY these research facts: 
    {facts}
    
    Format:
    - Main Title
    - Executive Summary(don't write word 'Executive Summary')
    - Key Findings (Bullet points)
    - Conclusion
    """
    response = llm.invoke(prompt)
    return {"final_report": response.content}

# --- 7. Router ---
def router(state: AgentState):
    status = state.get("review_status", "")
    if "REJECT" in status:
        return "researcher"
    return "writer"

# --- 8. Build Graph ---
workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("editor", editor_node)
workflow.add_node("writer", writer_node)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "editor")

workflow.add_conditional_edges(
    "editor",
    router,
    {
        "researcher": "researcher",
        "writer": "writer"
    }
)

workflow.add_edge("writer", END)
team_app = workflow.compile()