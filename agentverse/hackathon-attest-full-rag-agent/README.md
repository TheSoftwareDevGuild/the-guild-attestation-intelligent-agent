# Hackathon Attestation RAG Agent

This agent is responsible for querying a deployed RAG (Retrieval-Augmented Generation) backend API that provides intelligent answers about hackathons by leveraging a vectorized database of on-chain EAS (Ethereum Attestation Service) attestations.

## What it Does

The agent fetches relevant context from a vectorized database containing on-chain EAS attestations for hackathons and uses that context to answer questions about hackathons, projects, and developer activities. It provides intelligent insights based on real attestation data from the blockchain.

## Key Features

- **RAG Integration**: Connects to a deployed RAG backend API for intelligent question answering
- **Caching**: Implements response caching to optimize performance and reduce API calls
- **Context-Aware**: Uses vectorized attestation data to provide relevant, contextual answers
- **Error Handling**: Robust error handling for API failures and timeouts

## How it Works

1. **Query Processing**: Accepts natural language queries about hackathons and projects
2. **Context Retrieval**: The RAG backend searches through vectorized EAS attestation data
3. **Intelligent Response**: Generates answers based on relevant attestation context
4. **Caching**: Stores responses for 1 hour to avoid redundant API calls
5. **Logging**: Provides detailed logging of queries, answers, and context sources used

## Example Query

```
"Give me some successful hackathon ideas for DeFi"
```

This query would return insights about successful DeFi projects that have been attested on-chain, providing real examples and patterns from actual hackathon submissions.

## Configuration

The agent uses the following environment variables:
- `API_URL`: Backend API endpoint (default: "https://api-hackathon.theguild.dev")
- `API_PWD`: API password for authentication (default: "changeme123")

## Usage

The agent automatically queries the RAG backend on startup with a sample query and logs the response, including the number of context sources used to generate the answer.