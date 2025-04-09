import streamlit as st
import requests
import pandas as pd
from utils import fetch_text_from_url

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

st.title("📋 SHL Individual Assessment Recommender")
st.write("Input a natural language job description or paste a job URL to get relevant SHL test suggestions.")

# Input options
input_type = st.radio("Choose input type:", ["Text", "Job Description URL"])

user_input = ""
if input_type == "Text":
    user_input = st.text_area("Paste job description or role requirements:")
else:
    url = st.text_input("Paste job description URL:")
    if url:
        user_input = fetch_text_from_url(url)
        st.success("Fetched job description content from URL.")

if st.button("🔍 Recommend Tests"):
    if user_input.strip():
        with st.spinner("Getting recommendations from FastAPI..."):
            response = requests.post(
                "http://127.0.0.1:8000/recommend",  # Your FastAPI endpoint
                json={"query": user_input.strip()}
            )
            if response.status_code == 200:
                result = response.json()
                df = pd.DataFrame(result["recommended_assessments"])

                if not df.empty:
                    st.subheader("Top SHL Recommendations:")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No matching tests found.")
            else:
                st.error("Something went wrong with the API.")
    else:
        st.error("Please provide input.")
