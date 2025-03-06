import networkx as nx
from arango import ArangoClient
from pydantic import BaseModel
from typing import List
import json
from google import genai # pip install google-genai
from fuzzywuzzy import fuzz # pip install fuzzywuzzy
from fuzzywuzzy import process
import os
from dotenv import load_dotenv

load_dotenv()

google_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# เชื่อมต่อ ArangoDB
client = ArangoClient(hosts=os.getenv("ARANGO_HOST"))
db = client.db("JOB", username="root", password=os.getenv("ARANGO_PASSWORD"))

# สร้าง NetworkX DiGraph
G = nx.DiGraph()

# ดึง vertex และแยก _key
vertex_collections = ["job", "soft_skill", "hard_skill", "interest", "education"]
for vc in vertex_collections:
    query = f"FOR doc IN {vc} RETURN {{_key: doc._key, data: doc}}"
    cursor = db.aql.execute(query)
    for doc in cursor:
        G.add_node(doc["_key"], **{k: v for k, v in doc["data"].items() if k not in ["_key", "_id", "_rev"]})

# ดึง edge และแยก _key
edge_collections = ["requires_softskill", "requires_hardskill", "supported_by_interest", "enables_job"]
for ec in edge_collections:
    query = f"FOR doc IN {ec} RETURN {{source: SPLIT(doc._from, '/')[1], target: SPLIT(doc._to, '/')[1], data: doc}}"
    cursor = db.aql.execute(query)
    for doc in cursor:
        G.add_edge(doc["source"], doc["target"], **{k: v for k, v in doc["data"].items() if k not in ["_from", "_to", "_id", "_rev"]})

# ตรวจสอบโหนดและ edge
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

class JobSelector:
    def __init__(self):
        self.selected_job = []

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
                model="gemini-2.0-flash",
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

def fuzzy_mapping(preprocessed_json: dict, verbose=False):
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
    if verbose:
        print("Corrected additional data:", corrected_additional_data)
    return corrected_additional_data

def required_for_job(job, G):
    required_hard_skills = list(set([n for n, t, attr in G.in_edges(job, data=True) 
                                if attr['relation'] == 'hard_skill_leads_to']))
    required_soft_skills = list(set([n for n, t, attr in G.in_edges(job, data=True) 
                                if attr['relation'] == 'soft_skill_leads_to']))
    required_interests = list(set([n for n, t, attr in G.in_edges(job, data=True) 
                            if attr['relation'] == 'supports']))
    required_education = list(set([n for n, t, attr in G.in_edges(job, data=True) 
                            if attr['relation'] == 'enables_to']))
    return {
        "hard_skill": required_hard_skills,
        "soft_skill": required_soft_skills,
        "interest": required_interests,
        "education": required_education
    }

def merge_dicts(dict1, dict2):
    # Create a merged dictionary
    merged_dict = {}
    
    # Get all unique keys from both dictionaries
    all_keys = set(dict1.keys()).union(set(dict2.keys()))
    
    # For each key, merge the lists and remove duplicates
    for key in all_keys:
        merged_dict[key] = list(set(dict1.get(key, []) + dict2.get(key, [])))
    
    return merged_dict

def find_children(job, avg_salary, G, user_correct_json, job_selector:JobSelector):
    required = required_for_job(job, G)
    merge_required = merge_dicts(required, user_correct_json)
    results = find_best_job(merge_required, G)
    children = []
    for result in results['all_scores']:
        if len(children) >= 2:
            break
        else:
            if result['job_key'] not in job_selector.selected_job and result["attribute"]["average_salary"] > avg_salary:
                job_selector.selected_job.append(result['job_key'])
                children.append({
                    "job": result["attribute"]["job_title"],
                    "min_salary": result["attribute"]["min_salary"],
                    "max_salary": result["attribute"]["max_salary"],
                    "min_exp": result["attribute"]["min_exp"],
                    "max_exp": result["attribute"]["max_exp"],
                    "level": result["attribute"]["level"],
                    "category": result["attribute"]["category"],
                    "job_description": result["attribute"]["job_description"],
                    "hard_skill": result["hard_skill"],
                    "soft_skill": result["soft_skill"],
                    "interest": result["interest"],
                    "education": result["education"]
                })

    return children

def find_best_job(user_input, G):
    """
    user_input: dict containing lists of skills/interests/education
    """
    # ดึงเฉพาะ node ที่เป็น Job
    job_nodes = [n for n, attr in G.nodes(data=True) if attr['type'] == 'Job']
    
    # เก็บผลลัพธ์
    job_scores = []

    mapped_node = {}
    for key, att in G.nodes(data=True):
        mapped_node[key] = att['name']
    
    for job in job_nodes:
        # ดึง requirements
        required_hard_skills = set([n for n, t, attr in G.in_edges(job, data=True) 
                                  if attr['relation'] == 'hard_skill_leads_to'])
        required_soft_skills = set([n for n, t, attr in G.in_edges(job, data=True) 
                                  if attr['relation'] == 'soft_skill_leads_to'])
        required_interests = set([n for n, t, attr in G.in_edges(job, data=True) 
                                if attr['relation'] == 'supports'])
        required_education = set([n for n, t, attr in G.in_edges(job, data=True) 
                                if attr['relation'] == 'enables_to'])
        
        mapped_required_hard_skills = [mapped_node[hs] for hs in required_hard_skills]
        mapped_required_soft_skills = [mapped_node[ss] for ss in required_soft_skills]
        mapped_required_interests = [mapped_node[it] for it in required_interests]
        mapped_required_education = [mapped_node[edu] for edu in required_education]
        required = [mapped_required_hard_skills, mapped_required_soft_skills, mapped_required_interests, mapped_required_education]
        
        # แปลง user input เป็น set
        user_hard = set(user_input.get("hard_skill", []))
        user_soft = set(user_input.get("soft_skill", []))
        user_int = set(user_input.get("interest", []))
        user_edu = set(user_input.get("education", []))
        
        # คำนวณ matched และ missing
        matched_hard = len(user_hard & set(mapped_required_hard_skills))
        matched_soft = len(user_soft & set(mapped_required_soft_skills))
        matched_int = len(user_int & set(mapped_required_interests))
        matched_edu = len(user_edu & set(mapped_required_education))

        missing_hard = len(set(mapped_required_hard_skills) - user_hard)
        missing_soft = len(set(mapped_required_soft_skills) - user_soft)
        
        # NetworkX Algorithm: In-Degree
        in_degree = G.in_degree(job)  # จำนวน edges เข้า job (hard + soft)
        
        # คำนวณ score โดยเน้น hard_skill, soft_skill, และ in_degree
        score = (matched_hard * 10) + (matched_soft * 5) + (matched_int * 1) + (matched_edu * 0.5) - (missing_hard * 1) - (missing_soft * 0.5) - (in_degree * 0.5)

        avg_salary = (G.nodes[job]['min_salary']+G.nodes[job]['max_salary'])/2
        
        # ดึง attribute ของ job
        job_attribute = {
            "job_title": G.nodes[job]['name'],
            "category": G.nodes[job]['category'],
            "job_description": G.nodes[job]['job_description'],
            "min_salary": G.nodes[job]['min_salary'],
            "max_salary": G.nodes[job]['max_salary'],
            "min_exp": G.nodes[job]['min_exp'],
            "max_exp": G.nodes[job]['max_exp'],
            "level": G.nodes[job]['level'],
            "average_salary": avg_salary
        }
        
        # เก็บข้อมูล
        job_scores.append((job, score, matched_hard, matched_soft, missing_hard, missing_soft, in_degree, job_attribute, required))
    
    # เรียงลำดับตาม score
    sorted_jobs = sorted(job_scores, key=lambda x: x[1], reverse=True)
    
    # สร้างผลลัพธ์
    result = {
        'all_scores': [
            {
                'job_key': job,
                'score': score,
                'matched_hard': m_hard,
                'matched_soft': m_soft,
                'missing_hard': miss_hard,
                'missing_soft': miss_soft,
                'in_degree': in_deg,
                'attribute': attribute,
                'hard_skill': required[0],
                'soft_skill': required[1],
                'interest': required[2],
                'education': required[3]
            } for job, score, m_hard, m_soft, miss_hard, miss_soft, in_deg, attribute, required in sorted_jobs
        ]
    }
    
    return result

# API
def json_for_graph(user_input:str):
    job_selector = JobSelector()
    extracted_json = extract(user_input)
    corrected_json = fuzzy_mapping(extracted_json)
    results = find_best_job(corrected_json, G)
    for j in results['all_scores'][:3]:
        job_selector.selected_job.append(j['job_key'])
    json_response = {
        "nlq": user_input,
        "user_input": corrected_json,
        "nodes": [{
            "job": r["attribute"]["job_title"],
            "min_salary": r["attribute"]["min_salary"],
            "max_salary": r["attribute"]["max_salary"],
            "min_exp": r["attribute"]["min_exp"],
            "max_exp": r["attribute"]["max_exp"],
            "level": r["attribute"]["level"],
            "category": r["attribute"]["category"],
            "job_description": r["attribute"]["job_description"],
            "hard_skill": r["hard_skill"],
            "soft_skill": r["soft_skill"],
            "interest": r["interest"],
            "education": r["education"],
            "children": find_children(r["job_key"], r["attribute"]["average_salary"], G, corrected_json, job_selector)
        } for r in results['all_scores'][:3]]
    }

    return json_response

if __name__ == "__main__":
    user_input = "I have pyton skill, leadership, communicate and I love playing games. What job match me with some of my skill?"
    json_response = json_for_graph(user_input)
    # with open("json_output.json", "w") as f:
    #     json.dump(json_response, f, indent=4)

    print(json_response)