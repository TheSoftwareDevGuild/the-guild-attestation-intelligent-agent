"""
This agent is responsible for retrieving attestations from the RAG backend API.
"""

from uagents import Agent, Context, Model,Protocol,Model,Field
# from pydantic import Field
from typing import Optional, List
import os
import json
import requests
from datetime import datetime
from uuid import uuid4

agent = Agent()

class RetrieveAttestationRequest(Model):
    query: str
    #optional sender address
    sender: Optional[str] = None


class RetrieveAttestationResponse(Model):
    request_id: str = Field(..., description="The request ID")
    retrieved_context_ids: List[str] = Field(..., description="The IDs of the retrieved attestations")
    retrieved_context: List[str] = Field(..., description="The context of the retrieved attestations")
    similarity_scores: List[float] = Field(..., description="Similarity scores of the retrieved attestations")
    query: str = Field(..., description="The query that was used to retrieve the attestations")
    #optional sender address
    sender: Optional[str] = Field(..., description="The sender address")

attest_retrieval_proto = Protocol(name="attest_retrieval_protocol", version="1.0")

# Environment variables
API_URL = os.getenv("API_URL", "https://api-hackathon.theguild.dev")
API_PWD = os.getenv("API_PWD", "changeme123")

# Utility function to query the attest retrieval backend API
def query_attest_retrieval_backend(ctx, query: str, sender: str) -> dict or None:
    """Function to query the RAG retrieval backend API"""
    url = f"{API_URL}/rag/retrieve_context"
    payload = {
        "query": query,
        "password": API_PWD
    }
    
    # Check cache first
    cache_key = f"attest_retrieval_query_{hash(query)}"
    cached_data = ctx.storage.get(cache_key)
    if cached_data:
        data = json.loads(cached_data)
        # Cache for 1 hour
        if data.get("timestamp") and (datetime.utcnow().timestamp() - data["timestamp"]) < 3600:
            return data["response"]

    try:
        response = requests.post(url=url, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            # Cache the response
            ctx.storage.set(cache_key, json.dumps({
                "timestamp": datetime.utcnow().timestamp(),
                "response": data
            }))
            return RetrieveAttestationResponse(
                request_id=data["request_id"], 
                retrieved_context_ids=data["retrieved_context_ids"], 
                retrieved_context=data["retrieved_context"], 
                similarity_scores=data["similarity_scores"],
                sender=sender,
                query=query
            )
        else:
            ctx.logger.error(f"API Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        ctx.logger.error(f"Request failed: {e}")
    
    return None




@attest_retrieval_proto.on_message(model=RetrieveAttestationRequest, replies={RetrieveAttestationResponse})
async def handle_retrieve_attestation_request(ctx: Context, sender: str, msg: RetrieveAttestationRequest):
    """Handle RetrieveAttestationRequest messages, respond to sender with the retrieved attestations"""
    ctx.logger.info(f"Received RetrieveAttestationRequest from {sender} with query: {msg.query}")
    result = query_attest_retrieval_backend(ctx, msg.query, msg.sender)
    if result:
        response = RetrieveAttestationResponse(
            request_id=result["request_id"], 
            retrieved_context_ids=result["retrieved_context_ids"], 
            retrieved_context=result["retrieved_context"], 
            similarity_scores=result["similarity_scores"],
            sender=msg.sender,
            query=msg.query
        )
        ctx.logger.info(f"Sending RetrieveAttestationResponse to {sender} with {len(result['retrieved_context'])} attestations")
        await ctx.send(sender, response)
    else:
        response = RetrieveAttestationResponse(request_id=None, retrieved_context_ids=[], retrieved_context=[], similarity_scores=[])
        await ctx.send(sender, response)
    
# Include protocol in agent
agent.include(attest_retrieval_proto)

  
if __name__ == "__main__":
    agent.run()
    