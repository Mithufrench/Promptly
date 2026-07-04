"""
Promptly - AI DevOps Platform with Advanced Groq LLM Integration
Enterprise-Grade AI Assistant for Infrastructure & DevOps - v3.2
With Cognee Memory Integration for Persistent Agent Memory
With Dynamic LLM Model Manager for automatic model deprecation handling
"""
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
import sys
import json
from pathlib import Path
from typing import Optional, List, Dict
from groq import Groq
from memory_manager import init_memory_manager, get_memory_manager
from llm_model_manager import init_model_manager, get_model_manager, handle_model_decommission
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Promptly - AI DevOps Assistant", version="3.2.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM Model Manager for dynamic model handling
model_manager = None

# Initialize Groq client
GROQ_API_KEY = Config.GROQ_API_KEY
MODEL = Config.MODEL

if not GROQ_API_KEY:
    logger.warning("⚠️  GROQ_API_KEY not set. Set it as an environment variable.")
    client = None
else:
    client = Groq(api_key=GROQ_API_KEY)
    logger.info(f"✅ Groq client initialized with {MODEL} model")

# Global memory manager
memory_mgr = None

# ==================== AI SYSTEM PROMPTS ====================

SYSTEM_PROMPTS = {
    "devops_expert": """You are an expert DevOps Engineer and Cloud Architect. Your role is to provide:
1. Production-ready infrastructure designs
2. Best practices for containerization and orchestration
3. CI/CD pipeline recommendations
4. Security and compliance guidance
5. Cost optimization strategies
6. Performance tuning advice

Always provide:
- Specific, actionable recommendations
- Real-world considerations and trade-offs
- Code examples where applicable
- Links to official documentation when relevant
Format responses with clear sections and bullet points.""",

    "architect": """You are a Senior Software Architect specializing in cloud-native applications. Provide:
1. System design and architecture patterns
2. Scalability and performance considerations
3. Data architecture and database design
4. API design and microservices architecture
5. Technology stack recommendations

Focus on:
- Real production scenarios
- Trade-offs between different approaches
- Practical implementation advice
- Best practices from industry leaders
Always include diagrams in text format when helpful.""",

    "kubernetes_expert": """You are a Kubernetes and Container Orchestration Expert. Help with:
1. Kubernetes cluster design and setup
2. Pod deployment and management
3. Service mesh integration (Istio, Linkerd)
4. Monitoring and logging
5. Security policies and RBAC
6. Performance optimization

Provide:
- YAML configurations with explanations
- Troubleshooting guidance
- Production readiness checklists
- Cost optimization tips""",

    "infrastructure_coder": """You are an Infrastructure as Code (IaC) Expert. Specialize in:
1. Terraform configurations for various cloud providers (AWS, GCP, Azure)
2. CloudFormation templates
3. Ansible playbooks
4. ARM (Azure Resource Manager) templates
5. Pulumi Python/Go code

Requirements:
- Production-ready code
- Security best practices
- State management strategies
- Module design patterns
- Testing approaches for IaC""",

    "security_specialist": """You are a Cloud Security and DevSecOps Expert. Provide guidance on:
1. Security architecture and zero-trust design
2. Container and image security
3. Secrets management
4. Network security and firewalls
5. Compliance (GDPR, HIPAA, SOC2, PCI-DSS)
6. Incident response

Include:
- Specific security controls
- Threat models and mitigation
- Tools and technologies
- Audit and monitoring strategies"""
}

# ==================== DATA MODELS ====================

class ChatMessage(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    query: str
    agent_type: Optional[str] = "devops_expert"
    conversation_history: Optional[List[ChatMessage]] = None
    session_id: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    status: str = "success"
    agent_type: str = "devops_expert"
    model: str = MODEL
    tokens_used: Optional[Dict] = None
    from_memory: bool = False

class ArchitectureRequest(BaseModel):
    project_type: str
    requirements: str
    constraints: Optional[str] = None
    technologies: Optional[List[str]] = None

# ==================== AI PROCESSING FUNCTIONS ====================

def get_system_prompt(agent_type: str) -> str:
    """Get appropriate system prompt for agent type"""
    return SYSTEM_PROMPTS.get(agent_type, SYSTEM_PROMPTS["devops_expert"])

async def process_query_with_groq(query: str, agent_type: str = "devops_expert", 
                           conversation_history: Optional[List[ChatMessage]] = None,
                           session_id: Optional[str] = None) -> Dict:
    """Process query using Groq with conversation history and memory context"""
    if not client:
        return {
            "response": "Error: Groq API key not configured.",
            "status": "error",
            "agent_type": agent_type,
            "from_memory": False
        }
    
    try:
        logger.info(f"Processing query with agent: {agent_type}")
        
        messages = []
        from_memory = False
        
        # Add system message as first message
        system_prompt = get_system_prompt(agent_type)
        messages.append({
            "role": "system",
            "content": system_prompt
        })
        
        # Retrieve context from memory if enabled
        if Config.ENABLE_MEMORY_CONTEXT and memory_mgr and memory_mgr.enabled:
            try:
                context = await memory_mgr.get_agent_context(agent_type, session_id)
                if context:
                    logger.info(f"Retrieved context from memory for {agent_type}")
                    messages.append({
                        "role": "system",
                        "content": f"Relevant context from previous interactions:\n{context[:Config.MEMORY_CONTEXT_LIMIT]}"
                    })
                    from_memory = True
            except Exception as e:
                logger.warning(f"Failed to retrieve context from memory: {str(e)}")
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add current query
        messages.append({
            "role": "user",
            "content": query
        })
        
        # Get current model (which may have been auto-updated)
        current_model = model_manager.get_current_model() if model_manager else MODEL
        
        try:
            # Call Groq API
            response = client.chat.completions.create(
                model=current_model,
                max_tokens=2048,
                messages=messages
            )
            
            result_text = response.choices[0].message.content
            logger.info(f"Response generated by {agent_type} agent using {current_model}")
            
            # Store conversation in memory if enabled
            if Config.ENABLE_AGENT_LEARNING and memory_mgr and memory_mgr.enabled:
                try:
                    await memory_mgr.remember_conversation(
                        query=query,
                        response=result_text,
                        agent_type=agent_type,
                        session_id=session_id,
                        metadata={"model": current_model}
                    )
                    logger.info(f"Stored conversation in memory")
                except Exception as e:
                    logger.warning(f"Failed to store conversation: {str(e)}")
            
            return {
                "response": result_text,
                "status": "success",
                "agent_type": agent_type,
                "model": current_model,
                "tokens_used": {
                    "input": response.usage.prompt_tokens if hasattr(response, 'usage') else 0,
                    "output": response.usage.completion_tokens if hasattr(response, 'usage') else 0
                },
                "from_memory": from_memory
            }
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error calling Groq API: {error_msg}")
            
            # Check if it's a model decommissioned error
            if "decommissioned" in error_msg.lower() and model_manager:
                logger.warning(f"⚠️  Model {current_model} appears to be decommissioned!")
                new_model = await handle_model_decommission(e)
                
                if new_model:
                    logger.info(f"🔄 Automatically switching to {new_model}")
                    # Retry with new model
                    try:
                        response = client.chat.completions.create(
                            model=new_model,
                            max_tokens=2048,
                            messages=messages
                        )
                        result_text = response.choices[0].message.content
                        logger.info(f"✅ Response generated using fallback model {new_model}")
                        
                        return {
                            "response": result_text,
                            "status": "success",
                            "agent_type": agent_type,
                            "model": new_model,
                            "tokens_used": {
                                "input": response.usage.prompt_tokens if hasattr(response, 'usage') else 0,
                                "output": response.usage.completion_tokens if hasattr(response, 'usage') else 0
                            },
                            "from_memory": from_memory
                        }
                    except Exception as retry_error:
                        logger.error(f"Failed to retry with {new_model}: {str(retry_error)}")
            
            return {
                "response": f"Error processing query: {error_msg}",
                "status": "error",
                "agent_type": agent_type,
                "from_memory": False
            }
        
    except Exception as e:
        logger.error(f"Unexpected error in query processing: {str(e)}")
        return {
            "response": f"Error: {str(e)}",
            "status": "error",
            "agent_type": agent_type,
            "from_memory": False
        }

async def design_architecture(project_type: str, requirements: str, 
                       constraints: Optional[str] = None) -> Dict:
    """Generate architecture design using AI"""
    if not client:
        return {"status": "error", "message": "Groq not configured"}
    
    try:
        prompt = f"""Design a production-ready architecture for:

Project Type: {project_type}
Requirements: {requirements}
{f'Constraints: {constraints}' if constraints else ''}

Provide a comprehensive architecture including:
1. System architecture overview (describe as ASCII diagram if helpful)
2. Key components and their responsibilities
3. Data flow between components
4. Technology recommendations
5. Scalability approach
6. Monitoring and observability strategy
7. Security considerations
8. Cost optimization tips
9. Deployment strategy
10. Next implementation steps

Format with clear sections and actionable recommendations."""

        messages = [
            {"role": "system", "content": SYSTEM_PROMPTS["architect"]},
            {"role": "user", "content": prompt}
        ]
        
        current_model = model_manager.get_current_model() if model_manager else MODEL
        
        response = client.chat.completions.create(
            model=current_model,
            max_tokens=3000,
            messages=messages
        )
        
        return {
            "status": "success",
            "architecture": response.choices[0].message.content
        }
        
    except Exception as e:
        logger.error(f"Architecture design error: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

# ==================== API ENDPOINTS ====================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    global memory_mgr, model_manager
    
    logger.info(f"🚀 Starting Promptly - AI DevOps Assistant v3.2")
    logger.info(f"🔧 Environment: {Config.ENVIRONMENT}")
    logger.info(f"📊 Port: {Config.PORT}")
    logger.info(f"🤖 LLM Model: {MODEL}")
    logger.info(f"🔑 Groq API Key: {'✅ Set' if GROQ_API_KEY else '❌ Not set'}")
    logger.info(f"🧠 AI Agents: 5 specialized agents available")
    
    # Initialize Model Manager for dynamic model handling
    logger.info("🔄 Initializing LLM Model Manager for automatic deprecation handling...")
    model_manager = await init_model_manager(GROQ_API_KEY)
    logger.info("✅ LLM Model Manager initialized - will auto-switch on model deprecation")
    
    # Initialize memory manager
    if Config.COGNEE_ENABLED:
        logger.info(f"💾 Initializing Cognee Memory Layer...")
        memory_mgr = await init_memory_manager(
            enabled=Config.COGNEE_ENABLED,
            dataset_name=Config.COGNEE_DATASET
        )
        logger.info(f"✨ Cognee Memory integration: {'Enabled' if memory_mgr.enabled else 'Disabled (fallback to local cache)'}")
    else:
        logger.info("💾 Cognee Memory disabled (set COGNEE_ENABLED=true to enable)")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    memory_stats = {}
    if memory_mgr and memory_mgr.enabled:
        try:
            memory_stats = await memory_mgr.get_memory_stats()
        except:
            memory_stats = {"status": "unavailable"}
    
    model_stats = {}
    if model_manager:
        try:
            model_stats = await model_manager.health_check()
        except:
            model_stats = {"status": "unavailable"}
    
    return {
        "status": "healthy",
        "service": "promptly-ai",
        "name": "Promptly",
        "version": "3.2.0",
        "llm": "groq",
        "model": model_manager.get_current_model() if model_manager else MODEL,
        "ai_agents": list(SYSTEM_PROMPTS.keys()),
        "memory": memory_stats,
        "model_manager": model_stats
    }

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """Chat with Promptly AI Assistant"""
    try:
        logger.info(f"Chat request: {request.query[:100]}...")
        
        result = await process_query_with_groq(
            query=request.query,
            agent_type=request.agent_type,
            conversation_history=request.conversation_history,
            session_id=request.session_id
        )
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return QueryResponse(
            response=f"Error: {str(e)}",
            status="error",
            agent_type=request.agent_type,
            from_memory=False
        )

@app.get("/agents")
async def list_agents():
    """List available Promptly AI agents"""
    return {
        "agents": [
            {
                "type": agent_type,
                "description": f"Agent specialized in {agent_type.replace('_', ' ')}"
            }
            for agent_type in SYSTEM_PROMPTS.keys()
        ]
    }

@app.post("/agents/recommend")
async def recommend_agent(query: QueryRequest):
    """Recommend best agent for the query"""
    try:
        if not client:
            return {"recommended_agent": "devops_expert"}
        
        agent_selector_prompt = """Based on this query, recommend which specialist agent should handle it.
Choose from: devops_expert, architect, kubernetes_expert, infrastructure_coder, security_specialist

Return ONLY the agent type name, nothing else."""

        messages = [
            {"role": "system", "content": agent_selector_prompt},
            {"role": "user", "content": query.query}
        ]
        
        current_model = model_manager.get_current_model() if model_manager else MODEL
        
        response = client.chat.completions.create(
            model=current_model,
            max_tokens=50,
            messages=messages
        )
        
        recommended = response.choices[0].message.content.strip().lower()
        
        if recommended not in SYSTEM_PROMPTS:
            recommended = "devops_expert"
        
        return {
            "query": query.query[:100],
            "recommended_agent": recommended,
            "reason": f"This query is best handled by the {recommended} agent"
        }
        
    except Exception as e:
        logger.error(f"Agent recommendation error: {str(e)}")
        return {"recommended_agent": "devops_expert", "error": str(e)}

@app.post("/architecture/design")
async def design_app_architecture(request: ArchitectureRequest):
    """Design architecture for your application"""
    try:
        logger.info(f"Architecture design request for: {request.project_type}")
        
        result = await design_architecture(
            project_type=request.project_type,
            requirements=request.requirements,
            constraints=request.constraints
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Architecture error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/metrics")
async def metrics():
    """Get Promptly system metrics"""
    memory_stats = {}
    if memory_mgr:
        try:
            memory_stats = await memory_mgr.get_memory_stats()
        except:
            pass
    
    model_stats = {}
    if model_manager:
        try:
            model_stats = model_manager.get_model_stats()
        except:
            pass
    
    return {
        "agent_requests_total": 0,
        "agent_errors_total": 0,
        "agent_status": "running",
        "llm_provider": "groq",
        "model": model_manager.get_current_model() if model_manager else MODEL,
        "available_agents": len(SYSTEM_PROMPTS),
        "streaming_enabled": True,
        "conversation_support": True,
        "memory_stats": memory_stats,
        "model_stats": model_stats
    }

@app.get("/memory/stats")
async def memory_stats():
    """Get memory statistics"""
    if not memory_mgr:
        return {"status": "not_initialized"}
    
    return await memory_mgr.get_memory_stats()

@app.get("/model/stats")
async def model_stats():
    """Get LLM model manager statistics"""
    if not model_manager:
        return {"status": "not_initialized"}
    
    return model_manager.get_model_stats()

@app.get("/model/available")
async def available_models():
    """Get list of currently available Groq models"""
    if not model_manager:
        return {"status": "not_initialized"}
    
    models = await model_manager.get_available_models()
    best = await model_manager.get_best_available_model()
    
    return {
        "current_model": model_manager.get_current_model(),
        "available_models": models,
        "best_available_model": best,
        "model_count": len(models)
    }

# ==================== STATIC FILES ====================

app_dir = Path(__file__).parent
if (app_dir.parent / "frontend").exists():
    frontend_path = app_dir.parent / "frontend"
else:
    frontend_path = app_dir / "frontend"

logger.info(f"Frontend path: {frontend_path}")

if frontend_path.exists():
    try:
        app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")
        logger.info(f"✅ Static files mounted at /")
    except Exception as e:
        logger.error(f"Error mounting static files: {e}")

# ==================== STARTUP ====================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
