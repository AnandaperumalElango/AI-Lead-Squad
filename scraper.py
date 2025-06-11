import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re 
import random
# Mock function to generate leads for testing purposes
def mock_scrape_leads(keyword: str, num_leads: int = 10):
    """Generate mock leads based on a keyword input."""
    names = ["Alice Johnson", "Bob Smith", "Charlie Lee", "Diana Gomez", "Ethan Brown"]
    companies = ["TechNova", "HealthNet", "FinSmart", "RetailGen", "AutoEdge"]
    domains = ["technova.com", "healthnet.io", "finsmart.ai", "retailgen.co", "autoedge.tech"]
    descriptions = [
        "A SaaS company specializing in AI-driven analytics.",
        "A healthcare startup using machine learning for diagnostics.",
        "Fintech platform focused on blockchain-based payments.",
        "Retail automation company leveraging big data.",
        "Autonomous vehicle sensor startup."
    ]

    leads = []
    for _ in range(num_leads):
        idx = random.randint(0, 4)
        name = names[idx]
        email = f"{name.lower().replace(' ', '.')}@{domains[idx]}"
        company = companies[idx]
        desc = descriptions[idx]
        leads.append({
            "Name": name,
            "Email": email,
            "Company": company,
            "Description": desc
        })

    return leads

def _get_search_links(keyword, num_results, api_key):
    search_url = "https://serpapi.com/search"
    params = {
        "q": f"{keyword} site:linkedin.com OR site:crunchbase.com OR site:angel.co ",
        "num": num_results,
        "api_key": api_key,
        "engine": "google",
    }
    response = requests.get(search_url, params=params)
    data = response.json()
    links = []

    for result in data.get("organic_results", []):
        link = result.get("link")
        if link:
            links.append(link)

    return links

def _scrape_lead_data(url):
    lead = {
        "Name": "Unknown",
        "Email": "Not Found",
        "Company": "Unknown",
        "Description": "Not Available"
    }

    try:
        res = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if res.status_code != 200:
            return lead

        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        # Extract email
        emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", res.text))
        if emails:
            lead["Email"] = list(emails)[0]

        # Try to get title or h1 as name
        title_tag = soup.find("title")
        if title_tag:
            lead["Name"] = title_tag.text.strip()

        h1_tag = soup.find("h1")
        if h1_tag:
            lead["Company"] = h1_tag.text.strip()

        # Use first 500 characters of the text as description
        lead["Description"] = text[:500]

    except Exception:
        lead["Name"] = "Error"
        lead["Email"] = "Error"
        lead["Company"] = "Error"
        lead["Description"] = "Error"

    return lead

def serpapi_scrape_leads(keyword, num_results=10, api_key="20f55b61fa1caf400275a6c1259b3c436142cabba9a94b5c4a19df14c4d0fd81"):
    search_results = _get_search_links(keyword, num_results, api_key)
    leads = []
    for url in search_results:
        lead = _scrape_lead_data(url)
        lead['Website'] = url
        leads.append(lead)
    return leads

# import random
# import requests

# def mock_scrape_leads(keyword: str, num_leads: int = 10):
#     """Generate mock leads based on a keyword input."""
#     names = ["Alice Johnson", "Bob Smith", "Charlie Lee", "Diana Gomez", "Ethan Brown"]
#     companies = ["TechNova", "HealthNet", "FinSmart", "RetailGen", "AutoEdge"]
#     domains = ["technova.com", "healthnet.io", "finsmart.ai", "retailgen.co", "autoedge.tech"]
#     descriptions = [
#         "A SaaS company specializing in AI-driven analytics.",
#         "A healthcare startup using machine learning for diagnostics.",
#         "Fintech platform focused on blockchain-based payments.",
#         "Retail automation company leveraging big data.",
#         "Autonomous vehicle sensor startup."
#     ]

#     leads = []
#     for _ in range(num_leads):
#         idx = random.randint(0, 4)
#         name = names[idx]
#         email = f"{name.lower().replace(' ', '.')}@{domains[idx]}"
#         company = companies[idx]
#         desc = descriptions[idx]
#         leads.append({
#             "Name": name,
#             "Email": email,
#             "Company": company,
#             "Description": desc
#         })

#     return leads

# def serpapi_scrape_leads(query, num_leads, api_key="20f55b61fa1caf400275a6c1259b3c436142cabba9a94b5c4a19df14c4d0fd81"):
#     """
#     Scrapes Google search results using SerpAPI to generate real leads.
#     You must replace YOUR_SERPAPI_KEY with a valid key.
#     """
#     url = "https://serpapi.com/search"
#     params = {
#         "engine": "google",
#         "q": query,
#         "num": num_leads,
#         "api_key": api_key
#     }

#     response = requests.get(url, params=params)
#     results = response.json().get("organic_results", [])

#     leads = []
#     for r in results:
#         leads.append({
#             "Name": "Unknown",
#             "Email": "unknown@example.com",
#             "Company": r.get("source", "Unknown"),
#             "Description": r.get("snippet", r.get("title", "No description available"))
#         })

#     return leads
