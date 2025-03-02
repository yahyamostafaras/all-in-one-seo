import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import time

def keyword_research(keyword):
    """
    Fetch keyword suggestions from Google Search Autocomplete without an API.
    """
    url = f"https://www.google.com/search?q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return ["Error fetching keywords"]

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract suggestions (found inside Google search results page)
    suggestions = []
    for suggestion in soup.select("li span"):  # Common structure for suggestions
        text = suggestion.text.strip()
        if text and text.lower() != keyword.lower():  # Remove duplicate searches
            suggestions.append(text)
    
    return suggestions[:20]  # Limit to 10 suggestions

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
    word_count = len(text.split())
    readability_score = "Easy" if word_count < 200 else "Moderate"
    return {"word_count": word_count, "readability": readability_score}

st.title("SEO Automation Tool")

option = st.sidebar.selectbox("Choose a Task", ["Keyword Research", "On-Page SEO Analysis", "Backlink Monitoring", "Site Audit", "Rank Tracking", "Content Optimization"])

elif option == "Keyword Research":
    keyword = st.text_input("Enter a keyword")
    
    if st.button("Get Suggestions"):
        results = keyword_research(keyword)  # Calls the function
        st.write("🔎 **Keyword Suggestions:**")
        
        if results:
            for i, kw in enumerate(results):
                st.write(f"{i+1}. {kw}")  # Display results
        else:
            st.write("No suggestions found. Try a different keyword.")

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
