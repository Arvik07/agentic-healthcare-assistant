from langchain.tools import Tool
import wikipedia
import requests
from duckduckgo_search import DDGS

# ---------------- Wikipedia ----------------
def wiki_tool(query):
    try:
        return wikipedia.summary(query, sentences=3)
    except:
        return "No Wikipedia result found."

# ---------------- Web Search ----------------
def web_tool(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=2)
            return "\n".join([r["body"] for r in results])
    except:
        return "No web results found."

# ---------------- PubMed ----------------
def pubmed_tool(query):
    try:
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": 2
        }
        res = requests.get(url, params=params).json()
        ids = res["esearchresult"]["idlist"]

        if not ids:
            return "No PubMed results found."

        return f"Relevant PubMed IDs: {ids}"
    except:
        return "Error fetching PubMed data."

# ---------------- Drug Info (FIXED) ----------------
def drug_tool(query):
    try:
        url = f"https://api.fda.gov/drug/label.json?search={query}&limit=1"
        res = requests.get(url).json()

        if "results" in res:
            data = res["results"][0]
            return str(data.get("adverse_reactions", "No side effect data available"))[:300]

        return "No drug info found."
    except:
        return "Error fetching drug data."

# ---------------- BMI Calculator ----------------
def bmi_tool(query):
    try:
        parts = query.lower().split()
        weight = float(parts[parts.index("weight") + 1])
        height = float(parts[parts.index("height") + 1]) / 100

        bmi = weight / (height ** 2)

        return f"BMI is {bmi:.2f}"
    except:
        return "Provide input like: weight 70 height 170"

# ---------------- Tool List ----------------
tools = [
    Tool(
        name="Wikipedia",
        func=wiki_tool,
        description="Use for general medical knowledge like diseases, symptoms, definitions"
    ),
    Tool(
        name="WebSearch",
        func=web_tool,
        description="Use for latest healthcare news or updates"
    ),
    Tool(
        name="PubMed",
        func=pubmed_tool,
        description="Use for clinical research papers, trials, studies"
    ),
    Tool(
        name="DrugInfo",
        func=drug_tool,
        description="Use for drug side effects, adverse reactions, and usage"
    ),
    Tool(
        name="BMICalculator",
        func=bmi_tool,
        description="Use when user provides weight and height to calculate BMI"
    ),
]