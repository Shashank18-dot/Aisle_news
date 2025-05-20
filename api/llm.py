import os
from groq import Groq
from typing import List, Dict, Any

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(context: str, question: str) -> str:
    """
    Query the LLM with context and a question.
    
    Args:
        context: The context information (e.g., news articles)
        question: The user's question about the context
        
    Returns:
        str: The LLM's response
    """
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": """You are an AI-news analyst. Your task is to:
                    1. Analyze the provided news articles
                    2. Identify key themes and connections
                    3. Provide clear, concise summaries
                    4. Highlight important developments
                    5. Maintain factual accuracy
                    Focus on being informative and objective."""
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nUser question: {question}"
                }
            ],
            temperature=0.1,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error querying LLM: {str(e)}")

def summarize_articles(articles: List[Dict[str, Any]]) -> str:
    """
    Generate a summary of multiple articles.
    
    Args:
        articles: List of article dictionaries with title, content, etc.
        
    Returns:
        str: A summary of the articles
    """
    context = "\n\n".join([
        f"Title: {article['title']}\nContent: {article.get('description', '')}"
        for article in articles
    ])
    
    return ask_llm(
        context=context,
        question="Please provide a concise summary of these articles, highlighting the main points and any significant developments."
    ) 