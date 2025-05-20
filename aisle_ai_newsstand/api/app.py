from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Aisle AI Newsstand API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchQuery(BaseModel):
    query: str
    limit: Optional[int] = 5

@app.get("/")
async def root():
    return {"message": "Welcome to Aisle AI Newsstand API"}

@app.post("/search")
async def search_news(query: SearchQuery):
    try:
        # TODO: Implement RAG search logic
        return {"message": "Search endpoint", "query": query.query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 