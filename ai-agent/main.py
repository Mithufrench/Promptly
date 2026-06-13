"""
Lightweight AI Agent with FastAPI
No external API dependencies required
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Agent API", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    status: str = "success"

# Simple responses (no LLM needed)
def process_query(query: str) -> str:
    """Process user query with simple logic"""
    query_lower = query.lower()
    
    if "hello" in query_lower or "hi" in query_lower:
        return "Hello! I'm an AI assistant. How can I help?"
    elif "math" in query_lower or "calculate" in query_lower:
        return "I can help with math calculations. Try: 2 + 2"
    elif "terraform" in query_lower:
        return "I can help with Terraform infrastructure. Ask me anything!"
    elif "kubernetes" in query_lower:
        return "I can help with Kubernetes deployments and commands."
    elif "docker" in query_lower:
        return "I can help with Docker containerization. What do you want to know?"
    elif "devops" in query_lower:
        return "DevOps is my specialty! I can help with CI/CD, infrastructure, automation, and more."
    else:
        return f"You asked: {query}. I'm ready to assist with DevOps tasks!"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ai-agent", "version": "2.0.0"}

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """Chat with AI agent"""
    try:
        logger.info(f"Query: {request.query}")
        response = process_query(request.query)
        return QueryResponse(response=response, status="success")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return QueryResponse(response=f"Error: {str(e)}", status="error")

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return {
        "agent_requests_total": 0,
        "agent_errors_total": 0,
        "agent_status": "running"
    }

# Frontend path
frontend_path = Path(__file__).parent.parent / "frontend"

# Mount frontend static files FIRST
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
    logger.info(f"Frontend static files mounted from {frontend_path}")
else:
    logger.warning(f"Frontend directory not found at {frontend_path}")

# Serve HTML at root AFTER mounting static files
@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - serve frontend HTML"""
    index_file = frontend_path / "index.html"
    if index_file.exists():
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            logger.info("Serving frontend HTML from root")
            return html_content
        except Exception as e:
            logger.error(f"Error reading index.html: {str(e)}")
            return "<h1>Error loading website</h1>"
    else:
        logger.warning(f"index.html not found at {index_file}")
        # Fallback API response
        return """
        <h1>AI Agent API</h1>
        <p>Frontend not found. Available endpoints:</p>
        <ul>
            <li><a href="/health">/health</a> - Health check</li>
            <li><a href="/docs">/docs</a> - API documentation</li>
            <li>/chat - Chat endpoint (POST)</li>
            <li>/metrics - Prometheus metrics</li>
        </ul>
        """

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting AI Agent API on port {port}...")
    logger.info(f"Frontend available at http://0.0.0.0:{port}/")
    logger.info(f"API Docs available at http://0.0.0.0:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
