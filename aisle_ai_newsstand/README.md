# Aisle AI Newsstand

A modern news aggregator that uses AI to help you find and understand news articles. The system fetches news from various RSS feeds, processes them using embeddings, and provides a natural language search interface.

## Features

- Real-time news aggregation from multiple sources
- Natural language search using RAG (Retrieval Augmented Generation)
- Modern web interface built with Gradio
- Vector database for efficient semantic search
- Docker-based deployment

## Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)
- Git

## Quick Start

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/aisle_ai_newsstand.git
   cd aisle_ai_newsstand
   ```

2. Create a `.env` file in the root directory:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start the services:

   ```bash
   docker-compose up -d
   ```

4. Access the application:
   - Frontend: http://localhost:7860
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Project Structure

```
aisle_ai_newsstand/
├─ api/                 # FastAPI backend
│  ├─ app.py           # Main API application
│  ├─ fetch_feeds.py   # RSS feed fetcher
│  └─ requirements.txt # API dependencies
├─ frontend/           # Gradio frontend
│  └─ gradio_app.py    # Web interface
├─ feeds.yml           # RSS feed configuration
├─ docker-compose.yml  # Service orchestration
└─ README.md          # This file
```

## Development

### Local Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r api/requirements.txt
   ```

3. Run the services:

   ```bash
   # Terminal 1: API
   cd api
   uvicorn app:app --reload

   # Terminal 2: Frontend
   cd frontend
   python gradio_app.py

   # Terminal 3: Feed Fetcher
   cd api
   python fetch_feeds.py
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
