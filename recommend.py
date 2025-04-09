# recommend.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv("data/shl_catalog.csv")


vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["description"])

def recommend_assessments(query_text):
    query_vec = vectorizer.transform([query_text])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[::-1][:10]

    return df.iloc[top_indices][[
        "url", "adaptive", "description", "duration", "remote", "type"
    ]].reset_index(drop=True)
