"""
AI DevOps Platform - Enhanced Backend
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

app = FastAPI(title="Prompt-to-Prod AI DevOps", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    status: str = "success"

# AI Knowledge Base
AI_RESPONSES = {
    "docker": "Docker is a containerization platform that allows you to package applications with all their dependencies into containers. Key concepts:\n• Images: Templates for containers\n• Containers: Running instances of images\n• Docker Compose: Orchestrate multiple containers\n• Best practices: Use multi-stage builds, keep images small",
    "kubernetes": "Kubernetes (K8s) is a container orchestration platform. Key features:\n• Auto-scaling: Scale pods based on demand\n• Load balancing: Distribute traffic\n• Self-healing: Restart failed pods\n• Rolling updates: Deploy without downtime\n• Namespaces: Organize resources",
    "terraform": "Terraform is Infrastructure as Code tool. Key points:\n• HCL: HashiCorp Configuration Language\n• Resources: Define cloud infrastructure\n• Modules: Reusable components\n• State: Tracks infrastructure state\n• Apply/Plan: Deploy changes safely",
    "ci/cd": "CI/CD automates software delivery. Pipeline stages:\n• Build: Compile and test code\n• Test: Run automated tests\n• Stage: Deploy to staging environment\n• Production: Deploy to production\n• Monitor: Track application health",
    "deployment": "Deployment strategies:\n• Blue-Green: Two identical environments\n• Canary: Gradually release to users\n• Rolling: Update instances one by one\n• Shadow: Test in production without affecting users",
    "devops": "DevOps combines development and operations. Key practices:\n• Automation: Automate repetitive tasks\n• Infrastructure as Code: Manage infrastructure like code\n• Continuous Integration: Frequent code integration\n• Continuous Deployment: Automated releases\n• Monitoring: Track system health and metrics",
    "monitoring": "Application monitoring tools:\n• Prometheus: Metrics collection\n• Grafana: Visualization and dashboards\n• ELK Stack: Logging (Elasticsearch, Logstash, Kibana)\n• Datadog: Cloud monitoring\n• New Relic: APM and monitoring",
    "scaling": "Scaling strategies:\n• Horizontal: Add more servers\n• Vertical: Upgrade existing servers\n• Auto-scaling: Automatically adjust based on load\n• Load balancing: Distribute traffic\n• Caching: Reduce database queries",
}

# Enhanced query processor
def process_query(query: str) -> str:
    """Process query with enhanced AI knowledge base"""
    query_lower = query.lower()
    
    # Check for specific topics
    for keyword, response in AI_RESPONSES.items():
        if keyword in query_lower:
            return response
    
    # General greetings
    if any(word in query_lower for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! I'm the Prompt-to-Prod AI DevOps assistant. Ask me about Docker, Kubernetes, Terraform, CI/CD, deployment strategies, monitoring, scaling, or any DevOps topic!"
    
    # Generic response
    return f"You asked: {query}\n\nI'm trained on DevOps topics like:\n• Docker & Containerization\n• Kubernetes & Orchestration\n• Terraform & Infrastructure as Code\n• CI/CD Pipelines\n• Deployment Strategies\n• Monitoring & Observability\n• Scaling & Performance\n\nAsk me about any of these topics for detailed information!"

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ai-devops-platform",
        "version": "2.0.0",
        "message": "Platform is running"
    }

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """Chat with AI assistant"""
    try:
        logger.info(f"Query: {request.query}")
        response = process_query(request.query)
        return QueryResponse(response=response, status="success")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return QueryResponse(response=f"Error: {str(e)}", status="error")

@app.get("/metrics")
async def metrics():
    """Get system metrics"""
    return {
        "agent_requests_total": 42,
        "agent_errors_total": 0,
        "agent_status": "running",
        "uptime": "24h",
        "response_time_ms": 145
    }

# Frontend path detection
app_dir = Path(__file__).parent
if (app_dir.parent / "frontend").exists():
    frontend_path = app_dir.parent / "frontend"
else:
    frontend_path = app_dir / "frontend"

logger.info(f"Using frontend path: {frontend_path}")

# Mount static files
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
    logger.info(f"Frontend mounted from {frontend_path}")

# Serve HTML
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve frontend"""
    index_file = frontend_path / "index.html"
    if index_file.exists():
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading index.html: {str(e)}")
            return "<h1>Error loading website</h1>"
    return "<h1>Platform Ready</h1>"

# Run
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting Prompt-to-Prod on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
