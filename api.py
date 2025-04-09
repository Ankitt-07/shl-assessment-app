# api.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from recommend import recommend_assessments

app = FastAPI()

# CORS for external access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Input model
class QueryModel(BaseModel):
    query: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/recommend")
def recommend_api(query: QueryModel):
    results = recommend_assessments(query.query)

    formatted = [
        {
            "url": row["url"],
            "adaptive_support": row["adaptive"],
            "description": row["description"],
            "duration": int(row["duration"].replace(" mins", "").strip()) if isinstance(row["duration"], str) else row["duration"],
            "remote_support": row["remote"],
            "test_type": [row["type"]],
        }
        for _, row in results.iterrows()
    ]
    return {"recommended_assessments": formatted}
