from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, model_validator
from typing import List, Dict

from gen_graph import json_for_graph
from chatbot import chatbot

app = FastAPI(title="Job Skills Graph API")

class GenGraphNode(BaseModel):
    job: str
    min_salary: int
    max_salary: int
    min_exp: float
    max_exp: float
    level: str
    category: str
    job_description: str
    hard_skill: List[str]
    soft_skill: List[str]
    interest: List[str]
    education: List[str]
    children: List['GenGraphNode'] = []
    
    @model_validator(mode='after')
    def validate_salary_and_exp_range(self):
        # Validate salary range
        if self.min_salary > self.max_salary:
            raise ValueError("Minimum salary cannot be greater than maximum salary")
        
        # Validate experience range
        if self.min_exp > self.max_exp:
            raise ValueError("Minimum experience cannot be greater than maximum experience")
        
        # Validate level values
        allowed_levels = ["Junior", "Mid", "Senior", "Lead", "Executive"]
        if self.level not in allowed_levels:
            raise ValueError(f"Level must be one of {allowed_levels}")
            
        return self

GenGraphNode.model_rebuild()  # This rebuilds the model to handle the recursive reference

class ChatbotRequest(BaseModel):
    query: str

class ChatbotResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatbotResponse)
async def chat_endpoint(request: ChatbotRequest):
    """
    Process a chat query and return the response from the chatbot.
    """
    try:
        response = chatbot(request.query)
        return ChatbotResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://go-soft-hack-ui-9-343673271091.us-central1.run.app"],  # SvelteKit dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class GenGraphRequest(BaseModel):
    query: str

class GenGraphNode(BaseModel):
    job: str
    min_salary: int
    max_salary: int
    min_exp: float
    max_exp: float
    level: str
    category: str
    job_description: str
    hard_skill: List[str]
    soft_skill: List[str]
    interest: List[str]
    education: List[str]
    children: List['GenGraphNode'] = []

GenGraphNode.model_rebuild()  # This rebuilds the model to handle the recursive reference

class GenGraphResponse(BaseModel):
    nlq: str
    user_input: Dict[str, List[str]]
    nodes: List[GenGraphNode]

class NLQRequest(BaseModel):
    queries: List[str]

class JobNameRequest(BaseModel):
    job_names: List[str]

class GraphResponse(BaseModel):
    nodes: List[Dict]
    edges: List[Dict]

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/gen_graph", response_model=GenGraphResponse)
async def generate_graph(request: GenGraphRequest):
    """
    Generate a job skills graph based on user input query.
    """
    try:
        response = json_for_graph(request.query)
        # Additional validation if needed beyond Pydantic model validation
        validate_graph_nodes(response.nodes)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def validate_graph_nodes(nodes: List[GenGraphNode]):
    """
    Additional validation for graph nodes beyond the Pydantic model validation.
    """
    if not nodes:
        raise ValueError("Graph must contain at least one node")
    
    # Check for duplicate job titles
    job_titles = [node.job for node in nodes]
    if len(job_titles) != len(set(job_titles)):
        raise ValueError("Job titles must be unique at each level of the graph")
    
    # Validate each node's children
    for node in nodes:
        if node.children:
            validate_graph_nodes(node.children)


if __name__ == "__main__":
    import uvicorn
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
