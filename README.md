# Promptly - AI DevOps Assistant

## 🚀 Enterprise-Grade AI-Powered DevOps Platform

**Promptly** is an intelligent AI DevOps assistant that automates infrastructure provisioning, DevOps workflows, and architecture design. Powered by Groq's Mixtral LLM with 5 specialized AI agents.

## ✨ Key Features

- **🤖 5 Specialized AI Agents**
  - DevOps Expert: Infrastructure, CI/CD, deployment
  - Software Architect: System design, scalability
  - Kubernetes Expert: Container orchestration
  - Infrastructure Coder: Terraform, Ansible, IaC
  - Security Specialist: Security architecture, compliance

- **⚡ Real-Time AI Responses**
  - Powered by Groq's llama-3.3-70b-versatile model
  - Sub-second response times
  - Conversation memory & context awareness

- **🏗️ Complete DevOps Automation**
  - CI/CD pipeline generation
  - Infrastructure as Code (Terraform, Ansible)
  - Kubernetes manifest generation
  - Architecture design & recommendations

- **🎯 Intelligent Routing**
  - Auto-recommends best agent for your query
  - Multi-turn conversations
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
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│         Groq AI (llama-3.1-70b)             │
│  • Real-time responses                      │
│  • Multi-agent coordination                 │
│  • Architecture design generation           │
└─────────────────────────────────────────────┘

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
│   ├── main.py                 # AI agent with Groq integration
│   ├── requirements.txt         # Python dependencies
│   └── config.py               # Configuration
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

## 🚀 Quick Start

### Option 1: Deploy to Railway (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Promptly.git
cd Promptly

# 2. Set up your Groq API key
# Get it from: https://console.groq.com/keys

# 3. Connect to Railway
# Go to https://railway.app/dashboard
# Create new project → Connect GitHub repo

# 4. Set environment variable in Railway
GROQ_API_KEY=gsk_your_actual_key_here

# 5. Deploy - Railway auto-deploys on git push
git push origin main
```

### Option 2: Local Development

```bash
# 1. Clone repository
git clone https://github.com/yourusername/Promptly.git
cd Promptly

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r ai-agent/requirements.txt

# 4. Set environment variables
export GROQ_API_KEY="your_actual_key"
export MODEL="llama-3.3-70b-versatile"
export PORT=8000

# 5. Run the application
python ai-agent/main.py

# 6. Open browser
# Frontend: http://localhost:8000
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

All endpoints are available at `https://your-promptly-domain.railway.app`

### GET `/health`
Health check endpoint
```bash
curl https://your-promptly-domain.railway.app/health
```

### POST `/chat`
Chat with AI assistant
```bash
curl -X POST https://your-promptly-domain.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Generate a Docker CI/CD pipeline",
    "agent_type": "devops_expert"
  }'
```

### GET `/agents`
List available agents
```bash
curl https://your-promptly-domain.railway.app/agents
```

### POST `/agents/recommend`
Get AI's recommended agent for your query
```bash
curl -X POST https://your-promptly-domain.railway.app/agents/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Help me with Kubernetes"}'
```

### POST `/architecture/design`
Generate complete architecture design
```bash
curl -X POST https://your-promptly-domain.railway.app/architecture/design \
  -H "Content-Type: application/json" \
  -d '{
    "project_type": "E-commerce Platform",
    "requirements": "High availability, scalability, multi-region"
  }'
```

### GET `/metrics`
System metrics and status
```bash
curl https://your-promptly-domain.railway.app/metrics
```

## ⚙️ Configuration

### Environment Variables

```env
# Groq LLM Configuration
GROQ_API_KEY=gsk_your_actual_api_key          # Required!
MODEL=llama-3.3-70b-versatile                 # AI model

# Server Configuration
PORT=8000                                      # Port (auto-assigned on Railway)
ENVIRONMENT=production                         # production or development
LOG_LEVEL=INFO                                # Logging level

# Python Configuration
PYTHONUNBUFFERED=1                            # Real-time logging
```

### How to Get Groq API Key

1. Visit https://console.groq.com
2. Sign up (free account)
3. Go to API Keys section
4. Create new API key
5. Copy and use in your environment

## 🚀 Deployment on Railway

### Prerequisites
- GitHub account
- Groq API key
- Railway account (free tier available)

### Steps

1. **Fork/Clone Repository**
   ```bash
   git clone https://github.com/yourusername/Promptly.git
   cd Promptly
   ```

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial Promptly deployment"
   git push origin main
   ```

3. **Connect to Railway**
   - Go to https://railway.app/dashboard
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Choose your Promptly repository
   - Follow setup wizard

4. **Add Environment Variables**
   - In Railway dashboard
   - Click your service
   - Variables tab
   - Add `GROQ_API_KEY` with your actual key

5. **Deploy**
   - Railway auto-deploys when you push to GitHub
   - Watch deployment progress in dashboard
   - Get your live URL once deployment completes

## 📊 Monitoring

### Health Check
```bash
curl https://your-promptly-domain.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "promptly-ai",
  "name": "Promptly",
  "version": "3.1.0",
  "llm": "groq",
  "model": "llama-3.3-70b-versatile",
  "ai_agents": ["devops_expert", "architect", "kubernetes_expert", "infrastructure_coder", "security_specialist"]
}
```

## 🔒 Security

- ✅ API key secured via environment variables
- ✅ No credentials in code
- ✅ HTTPS/SSL enabled on Railway
- ✅ CORS configured for web requests
- ✅ Error messages don't leak sensitive info
- ✅ Rate limiting ready (implement if needed)

## 🛠️ Troubleshooting

### Application not responding
1. Check Railway deployment status
2. Verify GROQ_API_KEY is set in Railway variables
3. Check logs: Railway dashboard → Logs tab

### Model not working
- Ensure GROQ_API_KEY is set correctly
- Verify key hasn't expired
- Check API key permissions in Groq console

### Chat returning errors
1. Check Railway logs for error details
2. Verify Groq API key is valid
3. Try a simpler query first

## 📚 Technologies Used

- **Backend**: FastAPI (Python)
- **AI/LLM**: Groq + llama-3.3-70b-versatile
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

- [ ] Add streaming responses
- [ ] Support for multiple LLM providers
- [ ] User authentication & API keys
- [ ] Query history & analytics
- [ ] Advanced prompt engineering
- [ ] Integration with external tools
- [ ] Mobile app

## 📞 Support

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Email: support@promptly.ai

---

**Promptly** - Your AI DevOps Assistant. Always ready to help. 🚀
