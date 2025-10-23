# 🎨 Attestation Frontend UI

Streamlit frontend for the Attestation Intelligent Agent with chat interface.

## 📁 **Structure**
```
frontend/
├── src/                    # Streamlit source code
│   ├── app.py             # Main Streamlit application
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
# Using streamlit directly
streamlit run src/app.py --server.address 0.0.0.0 --server.port 8501

# Or using Docker
docker build -t attestation-frontend .
docker run -p 8501:8501 --env-file .env attestation-frontend
```

## 🚀 **Deployment**

### **Heroku Deployment**
```bash
# From project root
./deploy-frontend.sh
```

### **Environment Variables**
- `API_URL` - Backend API URL (auto-set for production)
- `OPENAI_API_KEY` - OpenAI API key (for client-side usage)
- `GROQ_API_KEY` - Groq API key (for client-side usage)
- `GOOGLE_API_KEY` - Google API key (for client-side usage)

## 🎯 **Features**

- **Chat Interface** - Interactive conversation with the AI
- **Settings Tab** - Password authentication
- **Suggestions Tab** - Context from RAG responses
- **Real-time Updates** - Live chat experience

## 🔧 **Dependencies**

- **Streamlit** - Web app framework
- **Requests** - HTTP client
- **Pydantic** - Data validation
- **Pydantic Settings** - Configuration management

## 🎨 **UI Components**

### **Sidebar**
- **Settings Tab** - Password input and authentication
- **Suggestions Tab** - Context from previous queries

### **Main Area**
- **Chat Interface** - Message history and input
- **Error Handling** - User-friendly error messages

## 🐛 **Troubleshooting**

### **Connection Issues**
- Check backend URL: `echo $API_URL`
- Verify backend is running: `curl $API_URL/health`

### **Authentication Issues**
- Check password in Settings tab
- Verify backend password configuration

### **Build Issues**
- Test locally first: `docker build -t attestation-frontend .`
- Check dependencies: `uv tree`
