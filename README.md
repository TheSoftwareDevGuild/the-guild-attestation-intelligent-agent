# Hackathon Attestations AI Agent by The Guild
*This is an EthOnline 2025 Hackathon projet*

## Project Presentation

We want to create an AI Agent to help Hackathon participants explore past Hackathon projects for inspiration. Also this Agent could act as a judge and emit attestations.

This project is in the context of a longer term project, [The Guild Attestation Intelligent Agent](./ATTESTATION_INTELLIGENT_AGENT.md), by [The Guild](theguild.dev)

### Problem Statement
Hackathons are a great way for devs to train their skills and build a portfolio.
Unfortunately, the data around that is scattered in multiple organization, which prevents discovery around past projects and portfolio building.

### Solution
Blockchain acts as the universal API (and EAS in this specific case) and is therefore the perfect solution.
Sprinkle some AI on top of it to digest the enormous amount of data and you get the Hackathon Attestations AI Agent.
The Hackathon Attestations AI Agent is an Agent that uses RAG on past Hackathon attestations to help participants navigate past projects.
It also uses votes and assessments from past hackathons to make their own judgement.

### Sponsor tracks
- Envio: to fetch massive amounts of attestation data
- ASI: to decentralize the AI stack
- Hardhat for the contracts?

**ASI Prize Eligibility**: This project demonstrates the full ASI ecosystem by deploying multi-agent RAG systems on Agentverse, making them discoverable through ASI One's chat interface, and building towards an AI judge using MeTTa for decentralized attestation validation.

**Envio Prize Eligibility**: This project showcases Envio's HyperSync capabilities by mining massive amounts of EAS attestation data from Arbitrum, processing 3,291 attestations including Devfolio credentials and quadratic voting data, and building a comprehensive RAG system that demonstrates the power of on-chain data extraction and analysis.

## Project Progress

### What we built

#### 🚀 Complete RAG Pipeline with On-Chain Data
Built a comprehensive RAG system that mines, processes, and serves hackathon attestation data from the blockchain:

**Data Mining & Processing:**
- **Envio Integration**: Used Envio's HyperSync to fetch massive amounts of EAS attestation events from Arbitrum
- **Data Enrichment**: Scraped and processed 1,556 Devfolio attestations and 1,735 quadratic voting attestations
- **Smart Data Processing**: Built custom pipelines to extract GitHub links, project descriptions, and hackathon metadata
- **Vector Database**: Uploaded processed data into Qdrant for semantic search capabilities

**Backend Architecture:**
- **FastAPI Backend**: Built robust REST API with `/rag` endpoint for query processing
- **Hybrid Search**: Implemented both semantic and keyword search for optimal retrieval
- **Context Management**: Smart context processing and ranking for relevant attestation data
- **Caching Layer**: Intelligent caching system for improved performance

**Frontend Interface:**
- **Streamlit Dashboard**: Created interactive web interface at https://hackathon-assistant.theguild.dev/
- **Real-time Queries**: Live RAG system for exploring hackathon projects
- **Analytics Dashboard**: Visual representation of attestation data and patterns

#### 🤖 Multi-Agent Architecture with ASI Integration

**Agentverse Deployment:**
- **RAG Client Agent**: Built with uAgents framework for chat interface and query processing
- **Retrieval Agent**: Specialized agent for context retrieval with intelligent caching
- **Agent Communication**: Implemented custom protocols for inter-agent communication
- **ASI One Integration**: Deployed agents on ASI's decentralized AI platform

**Technical Implementation:**
- **uAgents Framework**: Used for building decentralized agents with chat protocols
- **Custom Message Models**: Built `RetrieveAttestationRequest` and `RetrieveAttestationResponse` models
- **Agent Discovery**: Integrated with ASI One for automatic agent discovery and routing
- **Caching Strategy**: Implemented agent-level caching for improved performance

#### 🔧 Technology Stack & Integration

**Core Technologies:**
- **Envio HyperSync**: For efficient blockchain data extraction
- **Qdrant Vector DB**: For semantic search and similarity matching
- **FastAPI**: High-performance backend with automatic API documentation
- **Streamlit**: Rapid frontend development for data visualization
- **uAgents**: Decentralized agent framework for ASI integration
- **LangChain**: RAG pipeline orchestration and prompt management

**Partner Technology Benefits:**
- **Envio**: Enabled us to fetch massive amounts of attestation data efficiently, processing thousands of events in minutes
- **ASI**: Provided decentralized AI infrastructure, allowing us to deploy agents that can be discovered and used by anyone
- **Qdrant**: Offered superior vector search capabilities with hybrid search for both semantic and keyword matching

#### 🎯 Notable Technical Achievements

**Hacky but Effective Solutions:**
- **Smart Data Extraction**: Built custom regex patterns to extract GitHub URLs and project metadata from unstructured attestation data
- **Hybrid Search Implementation**: Combined semantic search with keyword matching for optimal retrieval accuracy
- **Agent Caching**: Implemented intelligent caching at the agent level to reduce API calls and improve response times
- **Multi-Agent Coordination**: Created seamless communication between specialized agents for different tasks

**Data Processing Pipeline:**
- Processed 3,291 total attestations from Arbitrum
- Extracted and vectorized project descriptions, GitHub links, and hackathon metadata
- Built comprehensive search index for semantic similarity matching
- Implemented real-time data updates and synchronization

**Deployment Architecture:**
- **Live RAG System**: https://hackathon-assistant.theguild.dev/
- **Agentverse Agents**: Deployed and discoverable through ASI One
- **Multi-Agent Communication**: Seamless interaction between RAG client and retrieval agents
- **Scalable Infrastructure**: Built for handling multiple concurrent users and queries

## Hackathon roles
- Data analysis and AI: Mine hackathon attestation data and build a RAG - (Antoine)
- Assist with Data Analysis and AI: Enrich RAG with github data, make an agent, help with ASI integration
- Front End: Display hackathon attestation data in a nice dashboard with analytics, create attestation request for the Agent
- Smart Contracts: Create a smart contract suite for a Registry of Hackathon submissions for the Agent. The Agent can then emit attestations for the submissions. Also we could have a voting dynamic to testify submission autenticity and prevent SPAM.