# API

## start server
```shell
python3 main.py
```

## API Specification
Job Graph API
Endpoint: /job_graph/ Method: POST Description: Creates a job graph based on natural language queries.
{
  "queries": ["Data Scientist", "Machine Learning Engineer"]
}

{
  "nodes": [
    {"id": "job1", "label": "Data Scientist"},
    {"id": "job2", "label": "Related Job"}
  ],
  "edges": [
    {"source": "job1", "target": "job2", "weight": 1}
  ]
}

Skill Graph API
Endpoint: /skill_graph/ Method: POST Description: Returns a skill graph for specified job names.
{
  "job_names": ["Data Scientist", "Machine Learning Engineer"]
}

{
  "nodes": [
    {"id": "skill1", "label": "Python"},
    {"id": "skill2", "label": "Data Analysis"}
  ],
  "edges": [
    {"source": "skill1", "target": "skill2", "weight": 1}
  ]
}

Error Responses
All endpoints may return a 500 status code with an error message in case of server errors:

{
  "detail": "Error message"
}