from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

from gen_graph import json_for_graph
from chatbot import chatbot

app = FastAPI(title="Job Skills Graph API")

class ChatbotRequest(BaseModel):
    query: str

class ChatbotResponse(BaseModel):
    response: str

@app.post("/chat/", response_model=ChatbotResponse)
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
    allow_origins=["http://localhost:5173"],  # SvelteKit dev server
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

@app.post("/job_graph/", response_model=GenGraphResponse)
async def create_job_graph(request: NLQRequest):
    """
    Create a job graph based on natural language queries.
    """
    try:
        return json_for_graph(request.queries[0])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    # try:
    #     # Mock implementation - replace with actual logic
    #     nodes = [
    #         {"id": "job1", "label": request.queries[0]},
    #         {"id": "job2", "label": "Related Job"}
    #     ]
    #     edges = [
    #         {"source": "job1", "target": "job2", "weight": 1}
    #     ]
    #     return GraphResponse(nodes=nodes, edges=edges)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

@app.post("/skill_graph/", response_model=GraphResponse)
async def get_skill_graph(job_names: List[str]):
    """
    Get skill graph based on job names.
    """
    try:
        # Mock implementation - replace with actual logic
        nodes = [
            {"id": "skill1", "label": "Python"},
            {"id": "skill2", "label": "Data Analysis"}
        ]
        edges = [
            {"source": "skill1", "target": "skill2", "weight": 1}
        ]
        return GraphResponse(nodes=nodes, edges=edges)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/gen_graph/", response_model=GenGraphResponse)
async def generate_graph(request: GenGraphRequest):
    """
    Generate a job skills graph based on user input query.
    """
    try:
        return json_for_graph(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
