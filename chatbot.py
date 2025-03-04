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
db = client.db("POC", username="root", password=os.getenv("ARANGO_PASSWORD"))

arango_graph = ArangoGraph(db)

# Configuration
api_key = os.getenv("GOOGLE_API_KEY")  # Your API key
model_name = "gemini-2.0-flash"  # Supports JSON output and complex reasoning

chat_history = {
    "user": [],  # เก็บ queries ของผู้ใช้
    "ai": []     # เก็บ responses ของ AI
}

google_client = genai.Client(api_key=api_key)

class Extract_feature(BaseModel):
    job: List[str]
    hard_skill: List[str]
    soft_skill: List[str]
    interest: List[str]
    education: List[str]

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
        query = f"FOR doc IN {vc} RETURN doc._key"
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

def rewrite_query_with_history(current_query: str, chat_history: Dict[str, List[str]]) -> str:
    # llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY"))
    llm = ChatOpenAI(temperature=0, model_name=os.getenv("GPT_MODEL", "gpt-4o-mini"), api_key=os.getenv("OPENAI_API_KEY"))
    # ถ้าไม่มี history ให้คืนค่า query เดิม
    if not chat_history["user"]:
        return current_query

    # สร้าง prompt สำหรับ LLM เพื่อสรุป query ใหม่จาก history และ query ปัจจุบัน
    prompt = f"""
    You are an AI tasked with rewriting a user's current query by incorporating relevant context from their chat history.
    Chat History:
    User Queries: {json.dumps(chat_history['user'])}
    AI Responses: {json.dumps(chat_history['ai'])}
    Current Query: {current_query}
    
    Instructions:
    1. Analyze the chat history and the current query.
    2. Rewrite the current query into a single, concise query that summarizes the user's intent, incorporating relevant details from the chat history.
    3. Ensure the rewritten query is natural, clear, and includes key elements (e.g., skills, jobs, interests) from both the history and current query.
    4. Return only the rewritten query as a string, without additional explanation.
    """
    
    response = llm.invoke(prompt)
    rewritten_query = response.content.strip()
    return rewritten_query

def text_to_aql_to_text(query: str, preprocessed_json: dict):
    # llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY"))
    llm = ChatOpenAI(temperature=0, model_name=os.getenv("GPT_MODEL", "gpt-4o-mini"), api_key=os.getenv("OPENAI_API_KEY"))

    chain = ArangoGraphQAChain.from_llm(
        llm=llm,
        graph=arango_graph,
        verbose=True,
        allow_dangerous_requests=True
    )

    # Combine the natural language query with preprocessed JSON context
    combined_input = (
    f"Natural Language Query: {query}\n"
    f"Preprocessed Data: {json.dumps(preprocessed_json)}\n"
    "Generate an AQL query based on the preprocessed data and the following database schema:\n"
    "- Nodes:\n"
    "  1. Job: {_key: job title, type: Job, min_salary: int, max_salary: int, min_exp: int, max_exp: int, level: [Junior, Mid, Senior], category: str, job_description: str}\n"
    "  2. hard_skill: {_key: skill name, type: hard_skill, category: str, description: str}\n"
    "  3. soft_skill: {_key: skill name, type: soft_skill, category: str, description: str}\n"
    "  4. interest: {_key: name of interest, type: interest, category: str}\n"
    "  5. education: {_key: name of education, type: education, category: str}\n"
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
    "5. Return the AQL query, explicitly showing the use of INBOUND or OUTBOUND as appropriate.\n"
    "6. Translate the query results into natural language, adapting to the query’s focus:\n"
    "   - If jobs are relevant, include job titles, salary ranges (min_salary to max_salary), and required experience (min_exp to max_exp). Explain the match by specifying which skills, interests, or education align with the job (e.g., 'This job requires Python, which you have, via an OUTBOUND requires_hardskill edge').\n"
    "   - If skills or interests are the focus, describe related skills, interests, or their connections to jobs, with explanations (e.g., 'The skill Python supports software engineering jobs via an OUTBOUND requires_hardskill edge'), still limiting to 5 results.\n"
    "7. If no relevant results are found, return 'No suitable results found based on the provided data,' with a brief reason (e.g., 'None of the provided skills or education match available jobs via OUTBOUND edges').\n"
)

    result = chain.invoke(combined_input)
    response = str(result["result"])

    # อัปเดต chat history
    chat_history["user"].append(query)
    chat_history["ai"].append(response)

    return response

def chatbot(query:str) -> str:
    rewrite_query = rewrite_query_with_history(query, chat_history)
    extracted_json = extract(rewrite_query, verbose=True)
    corrected_json = fuzzy_mapping(extracted_json)
    response = text_to_aql_to_text(rewrite_query, corrected_json)
    return response