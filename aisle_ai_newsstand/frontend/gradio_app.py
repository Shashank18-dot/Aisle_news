import gradio as gr
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

def search_news(query, limit=5):
    """Search news articles using the API"""
    try:
        response = requests.post(
            f"{API_URL}/search",
            json={"query": query, "limit": limit}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Create Gradio interface
with gr.Blocks(title="Aisle AI Newsstand") as demo:
    gr.Markdown("# 📰 Aisle AI Newsstand")
    gr.Markdown("Search through the latest news articles using natural language.")
    
    with gr.Row():
        query_input = gr.Textbox(
            label="Search Query",
            placeholder="Enter your search query...",
            lines=2
        )
    
    with gr.Row():
        limit_slider = gr.Slider(
            minimum=1,
            maximum=20,
            value=5,
            step=1,
            label="Number of Results"
        )
    
    search_button = gr.Button("Search")
    
    output = gr.JSON(label="Results")
    
    search_button.click(
        fn=search_news,
        inputs=[query_input, limit_slider],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860) 