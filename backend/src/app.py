from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

# Add exception handling for imports
try:
    from src.api.middleware import RequestIdMiddleware
    from src.api.endpoints import api_router
except ImportError as e:
    logging.error(f"Import error: {e}")
    raise

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

try:
    app.add_middleware(RequestIdMiddleware)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],    
        allow_headers=["*"],
    )
    
    app.include_router(api_router)
    logger.info("✅ All middleware and routes loaded successfully")
except Exception as e:
    logger.error(f"❌ Error setting up app: {e}")
    raise

@app.get("/health")
def health():
    return {"status": "healthy", "message": "API is running"}

@app.post("/")
def root(request:Request):
    return {"message":"API"}

