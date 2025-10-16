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

## Project Progress

### What we are reusing
This is a fork from an ai-bootcamp repository that includes a RAG example to navigate Amazon products.
It included:
- jupyter notebooks to explore and work on data
- steamlit front end to send questions to the RAG
- fastapi backend to handle rag requests
- qdrant and langsmith setup

### Additions

#### Attestation Data Mining
- Use HyperSync to fetch EAS Attest events
- Use EAS GraphQL to enrich this data with attestation data field
- Analyze attestations to look for patterns such as github links

Interesting Data:

Arbitrum
1735 quadratic attestations onchain: the votes for different projects
1556 attestations onchain "DEVFOLIO ONCHAIN CREDENTIALS ATTESTATIONS": You participated in hackathon X
- devfolio dataset of quadratic voting and attestations
- rag helps explore what has already been done and what was successful too

## Hackathon roles
- Data analysis and AI: Mine hackathon attestation data and build a RAG - (Antoine)
- Assist with Data Analysis and AI: Enrich RAG with github data, make an agent, help with ASI integration
- Front End: Display hackathon attestation data in a nice dashboard with analytics, create attestation request for the Agent
- Smart Contracts: Create a smart contract suite for a Registry of Hackathon submissions for the Agent. The Agent can then emit attestations for the submissions. Also we could have a voting dynamic to testify submission autenticity and prevent SPAM.