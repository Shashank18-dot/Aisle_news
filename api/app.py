from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from .llm import ask_llm, summarize_articles
from .vector_search import search_articles, get_search_context

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

class Article(BaseModel):
    title: str
    link: str
    description: Optional[str]
    published_at: Optional[str]
    feed_source: str
    feed_category: str

@app.get("/")
async def root():
    return {"message": "Welcome to Aisle AI Newsstand API"}

@app.get("/summarise")
async def summarise_news(topic: str, hours: int = 24):
    """
    Search for news articles and generate a summary.
    
    Args:
        topic: The search topic
        hours: How far back to search (in hours)
        
    Returns:
        Dictionary containing articles and summary
    """
    try:
        # Search for relevant articles
        articles = search_articles(topic=topic, hours=hours)
        
        if not articles:
            return {
                "bullets": "No relevant articles found for the given topic and time range."
            }
        
        # Get context for LLM
        context = get_search_context(articles)
        
        # Generate summary
        summary = ask_llm(
            context=context,
            question=f"Please provide a bullet-point summary of the key developments about {topic} from these articles."
        )
        
        return {
            "bullets": summary,
            "articles": articles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search_news(query: SearchQuery):
    try:
        # Search for relevant articles
        articles = search_articles(
            topic=query.query,
            limit=query.limit
        )
        
        # Get LLM summary of the articles
        context = get_search_context(articles)
        summary = summarize_articles(articles)
        
        return {
            "query": query.query,
            "articles": articles,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 