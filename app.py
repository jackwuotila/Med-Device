import streamlit as st
import requests
import openai
import os
import re

# Set OpenAI API key from Streamlit Secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Function to summarize research
def summarize_research(paper_text):
    if not OPENAI_API_KEY:
        return "API key not found. Add it to Streamlit Secrets."
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.Completion.create(
        model="gpt-4",
        prompt=f"Summarize this research: {paper_text}",
        max_tokens=100
    )
    return response["choices"][0]["text"]

# Function to search PubMed without BeautifulSoup
import requests

def search_pubmed(surgeon_name):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": surgeon_name,
        "retmax": 5,  # Number of results to return
        "retmode": "json"
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        return ["⚠️ Error fetching data from PubMed."]
    
    data = response.json()
    
    # Extract PubMed IDs
    pubmed_ids = data.get("esearchresult", {}).get("idlist", [])
    
    if not pubmed_ids:
        return ["❌ No research papers found."]
    
    # Fetch paper details
    paper_titles = []
    for pubmed_id in pubmed_ids:
        details_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        details_params = {"db": "pubmed", "id": pubmed_id, "retmode": "json"}
        details_response = requests.get(details_url, params=details_params)
        
        if details_response.status_code == 200:
            details_data = details_response.json()
            paper_title = details_data.get("result", {}).get(pubmed_id, {}).get("title", "No Title Found")
            paper_titles.append(paper_title)
    
    return paper_titles

# Streamlit UI
st.title("🧠 Surgeon Research & Sales Insights")

surgeon_name = st.text_input("Enter Surgeon Name")
if surgeon_name:
    st.subheader(f"🔎 Fetching Data for: {surgeon_name}")
    
    # Fetch PubMed research papers
    research_papers = search_pubmed(surgeon_name)
    
    if research_papers:
        st.subheader("📚 Latest Research Publications")
        for paper in research_papers:
            st.write(f"- {paper}")
            summary = summarize_research(paper) if OPENAI_API_KEY else "⚠️ AI summarization unavailable"
            st.write(f"📄 Summary: {summary}")
    else:
        st.write("❌ No research papers found.")
    
    # LinkedIn Search Link
    st.subheader("🔗 LinkedIn Profile Search")
    google_search_url = f"https://www.google.com/search?q={surgeon_name.replace(' ', '+')}+site:linkedin.com"
    st.write(f"[Search {surgeon_name} on LinkedIn]({google_search_url})")

st.write("\n---\n")
st.write("🔍 **A Tool for Sales Reps to Research Surgeons and Their Market**")
