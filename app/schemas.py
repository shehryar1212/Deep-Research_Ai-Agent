from pydantic import BaseModel

# This is the "Form" the user must fill out to use your API
class ResearchRequest(BaseModel):
    topic: str
    
# This is the "Form" our API will send back
class ResearchResponse(BaseModel):
    topic: str
    final_report: str
    status: str