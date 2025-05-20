import gradio as gr
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

def ui_call(topic: str, hours: int) -> str:
    """
    Call the backend API to get news summaries.
    
    Args:
        topic: The search topic
        hours: How far back to search (in hours)
        
    Returns:
        Formatted markdown with news summaries
    """
    try:
        response = requests.get(
            f"{API_URL}/summarise",
            params={"topic": topic, "hours": hours}
        )
        response.raise_for_status()
        return response.json()["bullets"]
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
demo = gr.Interface(
    fn=ui_call,
    inputs=[
        gr.Textbox(
            label="Topic",
            placeholder="Enter a topic to search for news...",
            lines=2
        ),
        gr.Slider(
            minimum=1,
            maximum=48,
            value=24,
            step=1,
            label="Hours to look back"
        )
    ],
    outputs=gr.Markdown(label="News Summary"),
    title="📰 Aisle-AI Newsstand",
    description="Search and summarize the latest news articles using AI.",
    examples=[
        ["Artificial Intelligence", 24],
        ["Climate Change", 12],
        ["Space Exploration", 48]
    ]
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860) 