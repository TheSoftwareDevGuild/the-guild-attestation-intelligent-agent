# The Guild Attestation Intelligent Agent (AI Agent)

## Project Presentation

We want to create an AI Agent to help The Guild explore, manage and create on-chain attestations.

See [The Guild](theguild.dev) for more information about The Guild, a peer‑run organization for software developers.

### Problem Statement
The goal of this Agent is to solve two problems The Guild has:
- Explore, navigate attestatios ([EAS](https://attest.org)): There are so many kind of attestations and they are hard to navigate. The Guild itself creates attestations for its users but an Agent could help organize them better.
- Create badges for Guild contributors. We currently have a lot of contributor activity and it is hard to keep u and more importantly assess contribution work and give appropriate badges for it.

### Solution
We build an AI Agent (RAG, Agentic System) that uses attestation history and also possibly relevant github history to solve these problems.
Considering having the Agent write a newslatter about attestations too.

## Work

TODO:
- [ ] Build an attestation dataset
- [ ] Build a "Best OSS Github repo code" dataset
- [ ] Build a RAG that would help navigate attestations
- [ ] Integrate github data into the RAG
- [ ] Agentic: fetch contributor code
- [ ] Agentic: decide to emit attestations for this code
- [ ] Solidity: build badge pointers