from langchain_community.graphs import ArangoGraph
from langchain_community.chains.graph_qa.arangodb import ArangoGraphQAChain
from arango import ArangoClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import List, Dict
import json
from google import genai # pip install google-genai
from fuzzywuzzy import fuzz # pip install fuzzywuzzy
from fuzzywuzzy import process
import os
from dotenv import load_dotenv

load_dotenv()

client = ArangoClient(hosts=os.getenv("ARANGO_HOST"))
db = client.db("JOB", username="root", password=os.getenv("ARANGO_PASSWORD"))

arango_graph = ArangoGraph(db)

# Configuration
api_key = os.getenv("GOOGLE_API_KEY")  # Your API key
model_name = "gemini-2.0-flash"  # Supports JSON output and complex reasoning

google_client = genai.Client(api_key=api_key)

class Extract_feature(BaseModel):
    job: List[str]
    hard_skill: List[str]
    soft_skill: List[str]
    interest: List[str]
    education: List[str]

def clean_key(key):
    key_str = str(key)
    return ''.join(c if c.isalnum() else '_' for c in key_str).strip('_').lower()

def extract(nlq: str, verbose=False) -> str:
    # Prompt specifying the task
    prompt = f"""
    You are an AI tasked with analyzing natural language input from a user and extracting specific details into a JSON format.
    User's input: {nlq}
    Identify and categorize the following from the user's input:
    - 'job': job titles or roles mentioned (e.g., Software Engineer, Teacher).
    - 'hard_skill': technical skills or specific abilities (e.g., programming languages, tools).
    - 'soft_skill': interpersonal or cognitive skills (e.g., problem-solving, leadership).
    - 'interest': hobbies or personal interests (e.g., gaming, reading).
    - 'education': fields of study or degrees (e.g., Mathematics, Computer Science).
    Return the result as a JSON object with these fields as arrays. If no information is found for a category, use an empty array [].
    Use your judgment to interpret the input accurately, even if the phrasing varies.
    Example: 'I have python, problem-solving and calculating skills. I also have leadership and I love playing games. I graduated from Mathematics' 
    """

    # Configuration for JSON output
    config = {
        "response_mime_type": "application/json",
        "response_schema": Extract_feature
    }

    # Generate content
    for _ in range(2):
        try:
            response = google_client.models.generate_content(
                model=model_name,
                contents=[prompt],
                config=config)
            raw_response = response.text
            if verbose:
                print(f"Original NLQ: {nlq}")
                print("Raw response:")
                print(raw_response)

            # Parse to ensure it’s valid JSON (optional, since schema enforces it)
            json_response = json.loads(raw_response)
            return json_response
        except Exception as e:
            if verbose:
                print(f"Error: {e}")
                print("Raw response (if available):", response.text if 'response' in locals() else "No response")

def fuzzy_mapping(preprocessed_json: dict):
    all_nodes = {}
    for vc in ["job", "soft_skill", "hard_skill", "interest", "education"]:
        query = f"FOR doc IN {vc} RETURN doc.name"
        cursor = db.aql.execute(query)
        all_nodes[vc] = [doc for doc in cursor]

    corrected_additional_data = {}
    for key, values in preprocessed_json.items():
        corrected_additional_data[key] = [
            process.extractOne(val, all_nodes[key], scorer=fuzz.token_sort_ratio)[0]
            for val in values if process.extractOne(val, all_nodes[key], scorer=fuzz.token_sort_ratio)[1] >= 50
        ]
    print("Corrected additional data:", corrected_additional_data)
    return corrected_additional_data

def text_to_aql_to_text(query: str, preprocessed_json: dict):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY"))
    # llm = ChatOpenAI(temperature=0, model_name=os.getenv("GPT_MODEL", "gpt-4o-mini"), api_key=os.getenv("OPENAI_API_KEY"))

    chain = ArangoGraphQAChain.from_llm(
        llm=llm,
        graph=arango_graph,
        verbose=True,
        allow_dangerous_requests=True
    )

    # Combine the natural language query with preprocessed JSON context
    combined_input = (
    f"Natural Language Query: {query}\n"
    f"Preprocessed Data for name attribute of node: {json.dumps(preprocessed_json)}\n"
    "Generate an AQL query based on the preprocessed data and the following database schema:\n"
    "- Nodes:\n"
    "  1. Job: {_key: startswith job_, type: Job, min_salary: int, max_salary: int, min_exp: int, max_exp: int, level: [Junior, Mid, Senior], category: str, job_description: str, name: job title}\n"
    "  2. hard_skill: {_key: startswith hard_, type: hard_skill, category: str, description: str, name: skill name}\n"
    "  3. soft_skill: {_key: startswith soft_, type: soft_skill, category: str, description: str, name: skill name}\n"
    "  4. interest: {_key: startswith int_, type: interest, category: str, name: interest name}\n"
    "  5. education: {_key: startswith edu_, type: education, category: str, name: education name}\n"
    "- Edges (direction matters):\n"
    "  1. requires_softskill: {_from: soft_skill/, _to: job/, relation: soft_skill_leads_to} (OUTBOUND from soft_skill to job)\n"
    "  2. requires_hardskill: {_from: hard_skill/, _to: job/, relation: hard_skill_leads_to} (OUTBOUND from hard_skill to job)\n"
    "  3. supported_by_interest: {_from: interest/, _to: job/, relation: supports} (OUTBOUND from interest to job)\n"
    "  4. enables_job: {_from: education/, _to: job/, relation: enables_to} (OUTBOUND from education to job)\n"
    "Instructions:\n"
    "1. Use the preprocessed JSON data (hard_skill, soft_skill, interests, education) to construct an AQL query based on the natural language query.\n"
    "2. Leverage edge relationships (e.g., requires_hardskill, enables_job) to connect the input data to relevant nodes (jobs, skills, interests, or education), paying careful attention to edge direction:\n"
    "   - Use OUTBOUND when traversing from skills, interests, or education to jobs (e.g., soft_skill -> job, hard_skill -> job).\n"
    "   - Use INBOUND when traversing from jobs to skills, interests, or education (e.g., job -> soft_skill), if applicable to the query.\n"
    "   - Respect the schema: edges are defined as OUTBOUND from skills/interests/education to jobs, so prioritize this direction unless the query explicitly requires reverse traversal.\n"
    "3. When matching jobs, allow flexibility: jobs should match at least one skill, interest, or education from the input data, not requiring all to be present.\n"
    "4. Limit the query results to a maximum of 5 objects.\n"
    "5. Internally generate the AQL query, but do not include it in the final response.\n"
    "6. Translate the query results into a natural, user-friendly response, avoiding technical terms like 'AQL', 'INBOUND', 'OUTBOUND', 'node', or 'edge':\n"
    "   - If jobs are relevant, provide a simple list of up to 5 job titles with details like salary range (e.g., '$50,000 - $70,000') and experience required (e.g., '2-5 years'), followed by a brief explanation of why they match (e.g., 'This job fits because you know Python, which is one of the skills it needs').\n"
    "   - If skills or interests are the focus, describe up to 5 related skills or interests and how they connect to potential jobs (e.g., 'Your skill in Python could help you with software engineering roles').\n"
    "   - Use conversational language, as if explaining to a non-technical person.\n"
    "7. If no relevant results are found, respond with a simple message like 'Sorry, I couldn’t find any matches for you,' followed by a brief reason (e.g., 'None of the skills or education you provided seem to connect to the jobs available').\n"
)

    result = chain.invoke(combined_input)
    response = str(result["result"])

    return response

def chatbot(query:str) -> str:
    extracted_json = extract(query, verbose=True)
    corrected_json = fuzzy_mapping(extracted_json)
    response = text_to_aql_to_text(query, corrected_json)
    return response

if __name__ == "__main__":
    query = "If I want to be a full-stack developer, what skills I should have?"
    result = chatbot(query)
    print(result)