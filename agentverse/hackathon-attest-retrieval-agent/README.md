# Hackathon On-Chain Attestation Retrieval Agent

A uAgents-based intelligent agent that provides semantic search and retrieval capabilities specifically for **hackathon on-chain attestations**. This agent enables efficient querying of attestation data through natural language queries with intelligent caching.

## Purpose

This agent specializes in retrieving context from hackathon on-chain attestations stored in the system. It acts as a bridge between the uAgents ecosystem and the RAG backend, providing semantic search capabilities for attestation data.

## Key Features

- **Semantic Search**: Query hackathon attestations using natural language
- **On-Chain Focus**: Specifically designed for on-chain hackathon attestation data
- **Intelligent Caching**: 1-hour cache for improved performance
- **Protocol-based Communication**: Uses uAgents protocol for message handling

## API Models

### RetrieveAttestationRequest
```python
class RetrieveAttestationRequest(BaseModel):
    query: str  # Natural language query for hackathon attestation search
```

### RetrieveAttestationResponse
```python
class RetrieveAttestationResponse(BaseModel):
    request_id: str  # Unique identifier for the request
    retrieved_context_ids: List[str]  # IDs of retrieved attestations
    retrieved_context: List[str]  # Context content of retrieved attestations
    similarity_scores: List[float]  # Similarity scores (0-1) for each result
```

## Configuration

- `API_URL`: Backend API URL (default: `https://api-hackathon.theguild.dev`)
- `API_PWD`: API password for authentication (default: `changeme123`)

## Usage

```python
# Send a query request
request = RetrieveAttestationRequest(query="Find hackathon attestations about DeFi projects")
await ctx.send(agent_address, request)
```

## Example Queries

- "Find hackathon attestations about DeFi projects"
- "Show me on-chain attestations for blockchain security projects"
- "Retrieve attestations related to hackathon winners"
- "Find attestations for projects using specific technologies"

## Integration

This agent is designed to work with other uAgents in the ecosystem and provides structured data for hackathon attestation analysis and retrieval.
