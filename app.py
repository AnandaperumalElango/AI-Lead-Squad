import streamlit as st
import pandas as pd
from scraper import mock_scrape_leads, serpapi_scrape_leads
from ai_logic import lead_scoring
from utils import is_valid_email, deduplicate_leads
import joblib

# Load ML model and vectorizer
model = joblib.load("lead_classifier.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

st.set_page_config(page_title="AI-LeadSquad", layout="wide")
st.title("🚀 AI-Powered B2B Lead Generation Tool")

# Sidebar input
keyword = st.sidebar.text_input("Enter keyword", "AI startups")
num_leads = st.sidebar.slider("Number of leads", 5, 20, 10)
use_real = st.sidebar.checkbox("Use Real Scraping (via SerpAPI)")
run_button = st.sidebar.button("Generate Leads")

# You must insert your real SerpAPI key here
SERPAPI_KEY = "20f55b61fa1caf400275a6c1259b3c436142cabba9a94b5c4a19df14c4d0fd81"  # 🔐 Replace with your actual key

if run_button:
    with st.spinner("Scraping and analyzing leads..."):
        # Step 1: Scrape leads
        if use_real:
            leads = serpapi_scrape_leads(keyword, num_leads, api_key=SERPAPI_KEY)
        else:
            leads = mock_scrape_leads(keyword, num_leads)

        # st.write(leads)
        print(f"Raw leads from SerpAPI: {leads}")


        # Step 2: Deduplicate
        leads = deduplicate_leads(leads)

        # Step 3: Enrich leads with score, validation, classification
        for lead in leads:
            desc = lead["Description"]
            lead["Score"] = lead_scoring(desc)
            lead["Valid Email"] = is_valid_email(lead["Email"])
            X_desc = vectorizer.transform([desc])
            lead["Industry"] = model.predict(X_desc)[0]

        # Step 4: Convert to DataFrame
        df = pd.DataFrame(leads)

        st.success(f"✅ {len(df)} leads generated!")
        st.dataframe(df)

        # Step 5: Export CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="ai_leads.csv",
            mime="text/csv"
        )
