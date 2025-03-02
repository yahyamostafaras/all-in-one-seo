import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import time
import spacy

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def keyword_research(keyword):
    """
    Fetch keyword suggestions from Google's Autocomplete API.
    """
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        suggestions = data[1]  # Extract keyword suggestions
        return suggestions if suggestions else ["No suggestions found."]
    else:
        return ["Error fetching keywords."]

def on_page_seo_analysis(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_title = soup.title.text if soup.title else "No title found"
    meta_desc = soup.find("meta", attrs={"name": "description"})
    desc_content = meta_desc["content"] if meta_desc else "No description found"
    headings = [h.text for h in soup.find_all(re.compile('^h[1-6]$'))]
    return {"title": meta_title, "description": desc_content, "headings": headings}

def backlink_monitoring(domain):
    return [f"https://example.com/link-to-{domain}", f"https://another.com/{domain}-review"]

def site_audit(url):
    broken_links = ["https://example.com/broken-link"]
    slow_pages = [url] if time.time() % 2 == 0 else []
    return {"broken_links": broken_links, "slow_pages": slow_pages}

def rank_tracking(keyword):
    return {"keyword": keyword, "rank": 10}

def content_optimization(text):
    """
    AI-powered content optimization using spaCy NLP.
    """
    doc = nlp(text)
    word_count = len(doc)
    readability_score = "Easy" if word_count < 200 else "Moderate"
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    keyword_freq = {k: keywords.count(k) for k in set(keywords)}
    return {"word_count": word_count, "readability": readability_score, "keyword_density": keyword_freq}

# Streamlit UI
st.title("SEO Automation Tool")

option = st.sidebar.selectbox("Choose a Task", 
    ["Keyword Research", "On-Page SEO Analysis", "Backlink Monitoring", 
     "Site Audit", "Rank Tracking", "Content Optimization"])

if option == "Keyword Research":
    keyword = st.text_input("Enter a keyword")
    if st.button("Get Suggestions"):
        results = keyword_research(keyword)
        st.write("🔎 **Keyword Suggestions:**")
        for i, kw in enumerate(results):
            st.write(f"{i+1}. {kw}")

elif option == "On-Page SEO Analysis":
    url = st.text_input("Enter URL")
    if st.button("Analyze"):
        st.write(on_page_seo_analysis(url))

elif option == "Backlink Monitoring":
    domain = st.text_input("Enter domain")
    if st.button("Check Backlinks"):
        st.write(backlink_monitoring(domain))

elif option == "Site Audit":
    url = st.text_input("Enter URL")
    if st.button("Audit Site"):
        st.write(site_audit(url))

elif option == "Rank Tracking":
    keyword = st.text_input("Enter keyword")
    if st.button("Track Rank"):
        st.write(rank_tracking(keyword))

elif option == "Content Optimization":
    text = st.text_area("Enter content")
    if st.button("Optimize"):
        st.write(content_optimization(text))
