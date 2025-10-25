import openai
#import instructor
import os
from pydantic import BaseModel, Field

class RAGUsedContext(BaseModel):
    id: str = Field(description="ID of the attestation")
    project_link: str = Field(..., description="The project link")
    project_description: str = Field(description="Short description of the project used to answer the question.")

class RAGGenerationResponseWithReferences(BaseModel):
    answer: str = Field(description="Answer to the question.")
    references: list[RAGUsedContext] = Field(description="List of attestations used to answer the question.")


def generate_answer(prompt):
    # call open ai without instructor
    client = openai.OpenAI(
        api_key=os.getenv("ASI_ONE_API_KEY", "No API key provided"),
        base_url= "https://api.asi1.ai/v1",  
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content

def process_context(context):

    formatted_context = ""

    for id, chunk in zip(
            context["retrieved_context_ids"], 
            context["retrieved_context"], 
        ):
        formatted_context += f"- ID: {id}, description: {chunk}\n"

    return formatted_context

def build_prompt(preprocessed_context, question):

    template = f"""
    You are a hackathon assistant that can answer questions about the hackathon projects.

    You will be given a question and a list of project attestations.

    Instructions:
    - You need to answer the question based on the provided context only.
    - Never use word context and refer to it as the available attestations.
    - As an output you need to provide:

    * The answer to the question based on the provided context.
    * The list of the IDs of the chunks that were used to answer the question. Only return the ones that are used in the answer.
    * Short description (1-2 sentences) of the item based on the description provided in the context.

    - The short description should have the name of the item.
    - The answer to the question should contain detailed information about the product and returned with detailed specification in bullet points.

    Context:
    {preprocessed_context}

    Question:
    {question}
    """

    return template