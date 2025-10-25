"""
This agent is responsible for querying the deployed RAG backend API, and using the retrieved attestations to answer questions.
"""
from uagents import Agent, Context, Protocol,Model, Field
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,    
    chat_protocol_spec,
)
#from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4
from rag_utils import build_prompt, generate_answer, process_context

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


# Initialize the chat protocol with the standard chat spec
chat_proto = Protocol(spec=chat_protocol_spec)

RETRIEVAL_AGENT_ADDRESS = "agent1qdvs0lj4lsp30fhhj8ljzz57ghfjdw2rjhehmzyke880ht2mnvz7cqhrgu4"

# Utility function to wrap plain text into a ChatMessage
def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )

def query_retrieval_agent(ctx, sender: str, query: str):
    """Function to query the RAG backend API"""
    request = RetrieveAttestationRequest(query=query,sender=sender)
    ctx.logger.info(f"Sending RetrieveAttestationRequest to {RETRIEVAL_AGENT_ADDRESS} with request: {request}")
    ctx.send(RETRIEVAL_AGENT_ADDRESS, request)

@attest_retrieval_proto.on_message(model=RetrieveAttestationResponse, replies=set())
async def handle_retrieve_attestation_response(ctx: Context, sender: str, msg: RetrieveAttestationResponse):
    """Check the status of RetrieveAttestationResponse to see if RetrieveAttestationRequest was successfull"""
    if msg.request_id:
        retrieved_context = msg
        preprocessed_context = process_context(retrieved_context)
        prompt = build_prompt(preprocessed_context, msg.query)
        answer = generate_answer(prompt)

        # had to comment this because instructor is not supported

        # display the used context using project_link and project_description
        # context_text = "Used context:\n"
        # for context in answer.references:
        #     ctx.logger.info(f"Used context: {json.dumps(context, indent=4)}")
        #     context_text += f"- {context.get('project_link', 'No project link provided')}\n{context.get('project_description', 'No project description provided')}\n"
        # context_count = len(msg.retrieved_context)
        
        # Create response message with RAG answer and used context
        #response_text = f"Based on the hackathon attestation data:\n\n{answer}\n\n(Used {context_count} context sources)\n\n{context_text}"
        response_message = create_text_chat(answer)
        await ctx.send(sender, response_message)
    else:
        ctx.logger.info(f"No attestations found for {msg.query}")
        error_message = create_text_chat("Sorry, I couldn't retrieve information from the RAG backend. Please try again later.")
        await ctx.send(sender, error_message)


# Handle incoming chat messages
@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Received message from {sender}")
    
    # Always send back an acknowledgement when a message is received
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id))
    
    # Process each content item inside the chat message
    for item in msg.content:
        # Marks the start of a chat session
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started with {sender}")
            welcome_message = create_text_chat("Hello! I'm the Hackathon Attestation RAG Agent. I can help you find information about hackathons and projects using on-chain attestation data. What would you like to know?")
            await ctx.send(sender, welcome_message)
        
        # Handles plain text messages (from another agent or ASI:One)
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Text message from {sender}: {item.text}")

            # Query the RAG retrieval agent with the user's message
            query_retrieval_agent(ctx, sender, item.text)
            
        
        # Marks the end of a chat session
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended with {sender}")
        # Catches anything unexpected
        else:
            ctx.logger.info(f"Received unexpected content type from {sender}")


# Handle acknowledgements for messages this agent has sent out
@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")



# Include the chat protocol and publish the manifest to Agentverse
agent.include(attest_retrieval_proto)
agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
