import sys
import os

# --- PATH SETUP (Crucial for Cloud Deployment) ---
# This tells Python: "Look for the 'app' folder one level up"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.team_agent import team_app  # Direct import of the Brain!

st.set_page_config(page_title="Deep Research AI Agent", page_icon="👾", layout="centered")

# --- Header ---
st.title("👾 Deep Research AI Agent")
st.markdown(" Run a self correcting Multi Agent System where a Researcher, Editor, and Writer collaborate to write deep researched reports.")
st.divider()

# --- Input ---
topic = st.text_input("Enter a research topic:", placeholder="e.g., The Future of Solid State Batteries")

if st.button("Start Research"):
    if not topic:
        st.warning("Please enter a topic first.")
    else:
        status_container = st.empty()
        status_container.info(f" Mission Initiated: '{topic}👀'")
        
        try:
            with st.spinner(" Scout is searching...  Critic is reviewing..."):
                
                # --- DIRECT CALL TO THE BRAIN ---
                initial_state = {"task": topic, "revision_count": 0}
                result = team_app.invoke(initial_state)
                
                final_report = result["final_report"]
                
            # Clear status
            status_container.empty()
            
            # Show Result
            st.success("Research Completed! ✅")
            st.markdown("## 📝 Final Report")
            st.markdown(final_report)
            
            
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")