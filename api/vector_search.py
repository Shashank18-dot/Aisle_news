import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Qdrant client
qdrant = QdrantClient(
    host=os.getenv("QDRANT_HOST", "localhost"),
    port=int(os.getenv("QDRANT_PORT", "6333"))
)

# Initialize sentence transformer for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed(text: str) -> List[float]:
    """Generate embeddings for a text string."""
    return model.encode(text).tolist()

def search_articles(
    topic: str,
    hours: int = 24,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Search for articles using vector similarity and time filter.
    
    Args:
        topic: The search query
        hours: How far back to search (in hours)
        limit: Maximum number of results to return
        
    Returns:
        List of article dictionaries
    """
    # Calculate time filter
    since = datetime.utcnow() - timedelta(hours=hours)
    
    # Perform vector search
    hits = qdrant.search(
        collection_name="ai_news_vec",
        query_vector=embed(topic),
        query_filter={
            "must": [
                {
                    "key": "published",
                    "range": {
                        "gte": since.isoformat()
                    }
                }
            ]
        },
        limit=limit
    )
    
    # Format results
    articles = []
    for i, hit in enumerate(hits):
        article = {
            "title": hit.payload["title"],
            "link": hit.payload["link"],
            "description": hit.payload.get("summary", ""),
            "published_at": hit.payload["published"],
            "feed_source": hit.payload["source"],
            "feed_category": hit.payload.get("category", "General"),
            "score": hit.score
        }
        articles.append(article)
    
    return articles

def get_search_context(articles: List[Dict[str, Any]]) -> str:
    """
    Format articles into a context string for the LLM.
    
    Args:
        articles: List of article dictionaries
        
    Returns:
        Formatted context string
    """
    return "\n\n".join(
        f"[{i+1}] {article['title']}\n{article['description']}"
        for i, article in enumerate(articles)
    ) 