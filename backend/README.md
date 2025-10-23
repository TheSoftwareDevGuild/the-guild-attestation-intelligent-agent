# 🚀 Attestation Backend API

FastAPI backend for the Attestation Intelligent Agent with RAG capabilities.

## 📁 **Structure**
```
backend/
├── src/                    # API source code
│   ├── app.py             # FastAPI application
│   ├── api/               # API endpoints and models
│   ├── rag/               # RAG pipeline
│   └── core/              # Configuration
├── pyproject.toml          # Dependencies
├── Dockerfile            # Container configuration
└── env.example           # Environment template
```

## 🛠️ **Local Development**

### 1. **Setup Environment**
```bash
# Copy environment template
cp env.example .env

# Edit with your values
nano .env
```

### 2. **Install Dependencies**
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 3. **Run Locally**
```bash
# Using uvicorn directly
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

# Or using Docker
docker build -t attestation-backend .
docker run -p 8000:8000 --env-file .env attestation-backend
```

## 🚀 **Deployment**

### **Heroku Deployment**
```bash
# From project root
./deploy-backend.sh
```

### **Environment Variables**
- `OPENAI_API_KEY` - OpenAI API key
- `GROQ_API_KEY` - Groq API key  
- `GOOGLE_API_KEY` - Google API key
- `QDRANT_URL` - Qdrant Cloud URL
- `QDRANT_API_KEY` - Qdrant API key
- `APP_PASSWORD` - Application password

## 📊 **API Endpoints**

- `GET /health` - Health check
- `POST /rag` - RAG query endpoint
- `GET /docs` - API documentation

## 🔧 **Dependencies**

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Qdrant Client** - Vector database
- **OpenAI** - LLM integration
- **Instructor** - Structured outputs
- **LangSmith** - Observability

## 🐛 **Troubleshooting**

### **Memory Issues**
- Use Basic dynos: `heroku ps:scale web=1:basic --app attestation-backend-api`
- Check logs: `heroku logs --app attestation-backend-api --tail`

### **Build Issues**
- Test locally first: `docker build -t attestation-backend .`
- Check dependencies: `uv tree`
