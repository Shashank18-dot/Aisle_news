from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Qdrant client
client = QdrantClient(
    host=os.getenv("QDRANT_HOST", "localhost"),
    port=int(os.getenv("QDRANT_PORT", "6333"))
)

def init_collection():
    """Initialize the Qdrant collection for news articles."""
    # Create collection if it doesn't exist
    client.recreate_collection(
        collection_name="ai_news_vec",
        vectors_config=models.VectorParams(
            size=384,  # Size for all-MiniLM-L6-v2 embeddings
            distance=models.Distance.COSINE
        )
    )
    
    # Create payload indexes
    client.create_payload_index(
        collection_name="ai_news_vec",
        field_name="published",
        field_schema=models.PayloadFieldSchema.DATETIME
    )
    
    client.create_payload_index(
        collection_name="ai_news_vec",
        field_name="source",
        field_schema=models.PayloadFieldSchema.KEYWORD
    )
    
    client.create_payload_index(
        collection_name="ai_news_vec",
        field_name="category",
        field_schema=models.PayloadFieldSchema.KEYWORD
    )

if __name__ == "__main__":
    init_collection()
    print("Qdrant collection initialized successfully!") 