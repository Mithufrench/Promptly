# Promptly - AI DevOps Assistant

## 🚀 Enterprise-Grade AI-Powered DevOps Platform

**Promptly** is an intelligent AI DevOps assistant that automates infrastructure provisioning, DevOps workflows, and architecture design. Powered by Groq's LLaMA 3.3-70b with 5 specialized AI agents and **Cognee knowledge graph memory** for persistent, context-aware conversations.

## ✨ Key Features

- **🤖 5 Specialized AI Agents**
  - DevOps Expert: Infrastructure, CI/CD, deployment
  - Software Architect: System design, scalability
  - Kubernetes Expert: Container orchestration
  - Infrastructure Coder: Terraform, Ansible, IaC
  - Security Specialist: Security architecture, compliance

- **🧠 Cognee Knowledge Graph Memory**
  - Persistent memory across sessions via Cognee v1.x
  - `cognee.remember()` stores every conversation to the knowledge graph
  - `cognee.recall()` retrieves semantically relevant past context
  - `cognee.forget()` clears memory on demand
  - Per-session isolation with graceful local cache fallback

- **⚡ Real-Time AI Responses**
  - Powered by Groq's llama-3.3-70b-versatile model
  - Automatic model fallback if a model is deprecated
  - Sub-second response times
  - Context-aware multi-turn conversations

- **🏗️ Complete DevOps Automation**
  - CI/CD pipeline generation
  - Infrastructure as Code (Terraform, Ansible)
  - Kubernetes manifest generation
  - Architecture design & recommendations

- **🎯 Intelligent Routing**
  - Auto-recommends best agent for your query
  - Multi-turn conversations with memory
  - Professional dashboard UI

## 🏛️ Architecture

```
┌─────────────────────────────────────────────┐
│         Promptly Web Dashboard              │
│    (Frontend: HTML/CSS/JavaScript)          │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      FastAPI Backend (Python)               │
│  • 5 AI Agent System                        │
│  • Groq LLM Integration                     │
│  • REST API Endpoints                       │
│  • WebSocket Support                        │
└───────────┬──────────────┬──────────────────┘
            │              │
┌───────────▼──────┐  ┌────▼────────────────────┐
│  Groq AI         │  │  Cognee Knowledge Graph  │
│  llama-3.3-70b   │  │  • cognee.remember()     │
│  • Fast inference│  │  • cognee.recall()       │
│  • Auto-fallback │  │  • cognee.forget()       │
│  • Multi-agent   │  │  • Session isolation     │
└──────────────────┘  └─────────────────────────┘

┌─────────────────────────────────────────────┐
│      Infrastructure (Railway)               │
│  • Docker containerization                  │
│  • Auto-scaling deployment                  │
│  • SSL/HTTPS support                        │
│  • Health checks & monitoring               │
└─────────────────────────────────────────────┘
```

## 📁 Project Structure

```
Promptly/
├── ai-agent/                    # Python FastAPI backend
│   ├── main.py                 # FastAPI app + 5 AI agents
│   ├── memory_manager.py       # Cognee v1.x knowledge graph integration
│   ├── requirements.txt        # Python dependencies (incl. cognee>=0.5.0)
│   └── config.py               # Configuration & env vars
├── frontend/                    # Web UI
│   ├── index.html              # Dashboard & chat interface
│   ├── script.js               # Interactive features
│   └── styles.css              # Professional styling
├── Dockerfile                   # Multi-stage container build
├── railway.json                 # Railway deployment config
├── Procfile                     # Process definition
├── docker-compose.yml           # Local dev environment
├── terraform/                   # Infrastructure as Code
├── ansible/                     # Configuration management
├── manifests/                   # Kubernetes resources
└── README.md                    # This file
```

## 🧠 Cognee Integration

Promptly uses [Cognee](https://github.com/topoteretes/cognee) as its memory backend. Every conversation is stored in a knowledge graph and retrieved semantically when the agent responds.

```python
# Store conversation to knowledge graph
await cognee.remember(memory_text, session_id=sid)

# Retrieve relevant past context
results = await cognee.recall("Previous devops interactions", session_id=sid)

# Clear memory
await cognee.forget(dataset="promptly_agent")
```

**Key properties:**
- Session-scoped: each user gets an isolated memory namespace
- Graceful fallback: if Cognee is unavailable, local cache takes over
- Persistent: memory survives container restarts (when Cognee DB is configured)

Verify it's working:
```bash
curl https://promptly.up.railway.app/health
# → "cognee_connected": true

curl https://promptly.up.railway.app/memory/stats
# → session counts, entry counts, cognee_connected status
```

## 🚀 Quick Start

### Option 1: Deploy to Railway (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/Mithufrench/Promptly.git
cd Promptly

# 2. Get your Groq API key from https://console.groq.com/keys

# 3. Connect to Railway
# Go to https://railway.app/dashboard
# Create new project → Deploy from GitHub → Select Promptly

# 4. Set environment variables in Railway dashboard
GROQ_API_KEY=gsk_your_actual_key_here

# 5. Railway auto-deploys on every git push
git push origin main
```

### Option 2: Local Development

```bash
# 1. Clone repository
git clone https://github.com/Mithufrench/Promptly.git
cd Promptly

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies (includes cognee>=0.5.0)
pip install -r ai-agent/requirements.txt

# 4. Set environment variables
export GROQ_API_KEY="your_actual_key"
export MODEL="llama-3.3-70b-versatile"
export PORT=8000

# 5. Run the application
python ai-agent/main.py

# 6. Open browser
# App:      http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 3: Docker Local

```bash
docker-compose up -d
# Access at http://localhost:8000
```

## 🤖 AI Agents Explained

### DevOps Expert
Generate production-ready CI/CD pipelines, infrastructure designs, and deployment strategies.

Example: *"Generate a GitHub Actions pipeline for a Node.js app with Docker and Kubernetes"*

### Software Architect
Design scalable system architectures with best practices and trade-off analysis.

Example: *"Design a microservices architecture for an e-commerce platform"*

### Kubernetes Expert
Create Kubernetes manifests, cluster configurations, and deployment strategies.

Example: *"Generate a Kubernetes deployment with health checks and auto-scaling"*

### Infrastructure Coder
Generate Terraform, Ansible, and CloudFormation code for infrastructure provisioning.

Example: *"Create Terraform code for AWS EKS cluster setup"*

### Security Specialist
Provide security architecture guidance and compliance recommendations.

Example: *"Design a zero-trust security architecture for cloud applications"*

## 🔗 API Endpoints

All endpoints are available at `https://promptly.up.railway.app`

### GET `/health`
```bash
curl https://promptly.up.railway.app/health
```

### POST `/chat`
```bash
curl -X POST https://promptly.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Generate a Docker CI/CD pipeline",
    "agent_type": "devops_expert",
    "session_id": "my-session-123"
  }'
```

### GET `/agents`
```bash
curl https://promptly.up.railway.app/agents
```

### POST `/agents/recommend`
```bash
curl -X POST https://promptly.up.railway.app/agents/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Help me with Kubernetes"}'
```

### POST `/architecture/design`
```bash
curl -X POST https://promptly.up.railway.app/architecture/design \
  -H "Content-Type: application/json" \
  -d '{
    "project_type": "E-commerce Platform",
    "requirements": "High availability, scalability, multi-region"
  }'
```

### GET `/memory/stats`
```bash
curl https://promptly.up.railway.app/memory/stats
```

### GET `/metrics`
```bash
curl https://promptly.up.railway.app/metrics
```

## ⚙️ Configuration

### Environment Variables

```env
# Groq LLM Configuration
GROQ_API_KEY=gsk_your_actual_api_key          # Required
MODEL=llama-3.3-70b-versatile                 # Auto-fallback if deprecated

# Server Configuration
PORT=8000                                      # Auto-assigned on Railway
ENVIRONMENT=production
LOG_LEVEL=INFO

# Python Configuration
PYTHONUNBUFFERED=1
```

### How to Get Groq API Key

1. Visit https://console.groq.com
2. Sign up (free account)
3. Go to API Keys → Create new key
4. Set as `GROQ_API_KEY` in Railway Variables tab

## 📊 Monitoring

### Health Check
```bash
curl https://promptly.up.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "promptly-ai",
  "name": "Promptly",
  "version": "3.2.0",
  "llm": "groq",
  "model": "llama-3.3-70b-versatile",
  "fallback_enabled": true,
  "ai_agents": ["devops_expert", "architect", "kubernetes_expert", "infrastructure_coder", "security_specialist"]
}
```

## 🔒 Security

- ✅ API key secured via environment variables (never in code)
- ✅ HTTPS/SSL enabled on Railway
- ✅ CORS configured for web requests
- ✅ Error messages don't leak sensitive info
- ✅ Per-session memory isolation via Cognee

## 🛠️ Troubleshooting

### Application not responding
1. Check Railway deployment status
2. Verify `GROQ_API_KEY` is set in Railway Variables tab
3. Check logs: Railway dashboard → Logs tab

### Model not working
- The app auto-switches to fallback models if the primary is deprecated
- Verify `GROQ_API_KEY` is valid at https://console.groq.com

### Cognee not connecting
- App falls back to local session cache automatically
- Check `/health` → `cognee_connected` field to see status

## 📚 Technologies Used

- **Backend**: FastAPI (Python, async)
- **AI/LLM**: Groq + llama-3.3-70b-versatile (with auto-fallback)
- **Memory**: Cognee v1.x knowledge graph (`cognee.remember/recall/forget`)
- **Frontend**: HTML/CSS/JavaScript
- **Deployment**: Railway, Docker
- **Infrastructure**: Terraform, Ansible, Kubernetes

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Submit pull request

## 🎯 Roadmap

- [ ] Streaming responses
- [ ] Multi-LLM provider support
- [ ] User authentication & API keys
- [ ] Query history & analytics
- [ ] Mobile app

## 📞 Support

- Issues: GitHub Issues
- Discussions: GitHub Discussions

---

**Promptly** — AI DevOps Assistant with persistent knowledge graph memory. 🚀
