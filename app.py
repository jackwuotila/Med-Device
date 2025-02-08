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
def search_pubmed(surgeon_name):
    url = f"https://pubmed.ncbi.nlm.nih.gov/?term={surgeon_name.replace(' ', '+')}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return []
    
    # Extract publication titles using regex
    titles = re.findall(r'(?<=class="docsum-title".*?>)(.*?)(?=</a>)', response.text)
    publications = [re.sub('<.*?>', '', title).strip() for title in titles[:5]]  # Clean up HTML tags
    
    return publications

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
