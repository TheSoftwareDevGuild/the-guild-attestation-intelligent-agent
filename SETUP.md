# 🚀 Attestation Intelligent Agent - Setup Guide

## 📁 **Project Structure**
```
project/
├── backend/                    # Backend API
│   ├── src/                   # API source code
│   ├── pyproject.toml         # Backend dependencies
│   ├── Dockerfile            # Backend container
│   └── env.example           # Backend environment template
├── frontend/                   # Frontend UI
│   ├── src/                  # Streamlit source code
│   ├── pyproject.toml        # Frontend dependencies
│   ├── Dockerfile           # Frontend container
│   └── env.example          # Frontend environment template
├── docker-compose.yml         # Local development
├── deploy-backend.sh         # Backend deployment
├── deploy-frontend.sh        # Frontend deployment
├── set_backend_env.sh        # Backend environment setup
└── set_frontend_env.sh       # Frontend environment setup
```

## 🛠️ **Local Development Setup**

### 1. **Environment Setup**
```bash
# Copy environment templates
cp backend/env.example backend/.env
cp frontend/env.example frontend/.env

# Edit the .env files with your actual values
nano backend/.env
nano frontend/.env
```

### 2. **Run Locally**
```bash
# Start all services
docker-compose up

# Or run individually
docker-compose up backend
docker-compose up frontend
```

## 🚀 **Heroku Deployment**

### 1. **Set Environment Variables**
```bash
# Set backend environment variables
./set_backend_env.sh

# Set frontend environment variables
./set_frontend_env.sh
```

### 2. **Deploy Services**
```bash
# Deploy backend (builds & pushes from backend/)
./deploy-backend.sh

# Deploy frontend (builds & pushes from frontend/)
./deploy-frontend.sh
```

## 🔧 **Environment Variables**

### **Backend (.env)**
- `OPENAI_API_KEY` - OpenAI API key
- `QDRANT_URL` - Qdrant Cloud URL
- `QDRANT_API_KEY` - Qdrant API key
- `APP_PASSWORD` - Application password

### **Frontend (.env)**
- `API_URL` - Backend API URL (auto-set for production)

## 📊 **Benefits of This Structure**

1. **Smaller Docker Images** - Each service only includes its dependencies
2. **Faster Builds** - Less dependencies to install
3. **Better Caching** - Docker layers are more efficient
4. **Independent Scaling** - Each service can be scaled separately
5. **Cleaner Deployment** - Use `--context-path` instead of copying files
6. **Separation of Concerns** - Backend and frontend have their own configs

## 🐛 **Troubleshooting**

### **Memory Issues**
- Use Basic dynos: `heroku ps:scale web=1:basic --app <app-name>`
- Check logs: `heroku logs --app <app-name> --tail`

### **Build Issues**
- Check Dockerfile syntax
- Verify dependencies in pyproject.toml
- Test locally first: `docker-compose up`

### **Environment Issues**
- Verify .env files exist
- Check Heroku config: `heroku config --app <app-name>`
- Restart apps: `heroku restart --app <app-name>`
