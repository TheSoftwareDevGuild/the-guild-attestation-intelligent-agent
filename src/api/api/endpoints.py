from fastapi import APIRouter, Request, HTTPException, status
from src.api.api.models import RAGUsedContext, RAGRequest, RAGResponse
from src.api.core.config import config
import logging
from api.rag.retrieval_generation import rag_pipeline_wrapper



logger=logging.getLogger(__name__)  
rag_router=APIRouter()

@rag_router.post("/")
def rag(
    request: Request,
    payload: RAGRequest
) -> RAGResponse:
    
    # Verify password
    if payload.password != config.APP_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    answer = rag_pipeline_wrapper(payload.query)

    return RAGResponse(
        request_id=request.state.request_id,
        answer=answer["answer"],
        used_context=[RAGUsedContext(**used_context) for used_context in answer["used_context"]]
    )

api_router=APIRouter()
api_router.include_router(rag_router,prefix="/rag",tags=["rag"])