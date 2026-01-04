from fastapi import FastAPI
from app.schemas import ResearchRequest, ResearchResponse
from app.team_agent import team_app
# 1. Initialize the App
app = FastAPI(title="Deep Research Agent API")

# 2. Define the Route (The URL)
@app.post("/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest):
    
    # Run the new Graph Team
    # We initialize the state with the user's task
    initial_state = {"task": request.topic, "revision_count": 0}
    result = team_app.invoke(initial_state)
    
    return ResearchResponse(
        topic=request.topic,
        final_report=result["final_report"], # The Writer's output
        status="completed"
    )

# 5. Basic Health Check 
@app.get("/")
def home():

    return {"message": "Deep Research API is Online 🟢"}
