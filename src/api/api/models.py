from pydantic import BaseModel, Field
from typing import Optional, List


class RAGRequest(BaseModel):
    query: str = Field(..., description="The query to be used in the RAG pipeline")
    password: str = Field(..., description="Application password for authentication")


class RAGUsedContext(BaseModel):
    attester: str = Field(..., description="The attester address")
    project_link: str = Field(..., description="The project link")
    project_description: str = Field(..., description="The project description")

class RAGResponse(BaseModel):
    request_id: str = Field(..., description="The request ID")
    answer: str = Field(..., description="The answer to the query")
    used_context: List[RAGUsedContext] = Field(..., description="Information about attestations used to answer the query")