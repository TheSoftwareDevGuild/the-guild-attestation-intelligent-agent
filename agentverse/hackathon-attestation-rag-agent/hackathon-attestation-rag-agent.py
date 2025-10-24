"""
This agent is responsible for querying the deployed RAG backend API.
"""
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)
import json
import requests
import os
from datetime import datetime
from uuid import uuid4

agent = Agent()

# Initialize the chat protocol with the standard chat spec
chat_proto = Protocol(spec=chat_protocol_spec)

# Environment variables
API_URL = os.getenv("API_URL", "https://api-hackathon.theguild.dev")
API_PWD = os.getenv("API_PWD", "changeme123")

# Utility function to wrap plain text into a ChatMessage
def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )

def query_rag_backend(ctx, query: str) -> dict or None:
    """Function to query the RAG backend API"""
    url = f"{API_URL}/rag"
    payload = {
        "query": query,
        "password": API_PWD
    }
    
    # Check cache first
    cache_key = f"rag_query_{hash(query)}"
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
            return data
        else:
            ctx.logger.error(f"API Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        ctx.logger.error(f"Request failed: {e}")
    
    return None


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
            
            # Query the RAG backend with the user's message
            rag_response = query_rag_backend(ctx, item.text)
            
            if rag_response:
                answer = rag_response.get('answer', 'No answer provided')
                # display the used context using project_link and project_description
                context_text = "Used context:\n"
                for context in rag_response.get('used_context', []):
                    ctx.logger.info(f"Used context: {json.dumps(context, indent=4)}")
                    context_text += f"- {context.get('project_link', 'No project link provided')}\n{context.get('project_description', 'No project description provided')}\n"
                context_count = len(rag_response.get('used_context', []))
                
                # Create response message with RAG answer and used context
                response_text = f"Based on the hackathon attestation data:\n\n{answer}\n\n(Used {context_count} context sources)\n\n{context_text}"
                response_message = create_text_chat(response_text)
                await ctx.send(sender, response_message)
            else:
                error_message = create_text_chat("Sorry, I couldn't retrieve information from the RAG backend. Please try again later.")
                await ctx.send(sender, error_message)
        
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


@agent.on_event("startup")
async def query_rag_data(ctx: Context):
    """Query the RAG backend and log the response"""
    query = "What are some innovative DeFi projects that have been attested?"
    data = query_rag_backend(ctx, query)
    
    if data:
        ctx.logger.info(f"RAG Query: {query}")
        ctx.logger.info(f"Answer: {data.get('answer', 'No answer provided')}")
        if data.get('used_context'):
            ctx.logger.info(f"Used {len(data['used_context'])} context sources")
            ctx.logger.info(f"Used context: {json.dumps(data['used_context'], indent=4)}")

    else:
        ctx.logger.error("Failed to get response from RAG backend")


# Include the chat protocol and publish the manifest to Agentverse
agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
