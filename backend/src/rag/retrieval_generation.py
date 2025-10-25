import openai
import instructor
import numpy as np

from pydantic import BaseModel, Field
from langsmith import traceable, get_current_run_tree

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, Prefetch, FusionQuery, Document

from rag.utils.prompt_management import prompt_template_config
from src.core.config import config


class RAGUsedContext(BaseModel):
    id: str = Field(description="ID of the attestation")
    project_link: str = Field(..., description="The project link")
    project_description: str = Field(description="Short description of the project used to answer the question.")

class RAGGenerationResponseWithReferences(BaseModel):
    answer: str = Field(description="Answer to the question.")
    references: list[RAGUsedContext] = Field(description="List of attestations used to answer the question.")


@traceable(
    name="embed_query",
    run_type="embedding",
    metadata={"ls_provider": "openai", "ls_model_name": "text-embedding-3-small"}
)
def get_embedding(text, model="text-embedding-3-small"):
    response = openai.embeddings.create(
        input=text,
        model=model,
    )

    current_run = get_current_run_tree()

    if current_run:
        current_run.metadata["usage_metadata"] = {
            "input_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens
        }

    return response.data[0].embedding


@traceable(
    name="retrieve_data",
    run_type="retriever"
)
def retrieve_data(query, qdrant_client, k=5):

    query_embedding = get_embedding(query)

    results = qdrant_client.query_points(
        collection_name="Hackathon-attestation-collection-01-hybrid-search",
        prefetch=[
            Prefetch(
                query=query_embedding,
                using="text-embedding-3-small",
                limit=20
            ),
            Prefetch(
                query=Document(
                    text=query,
                    model="qdrant/bm25"
                ),
                using="bm25",
                limit=20
            )
        ],
        query=FusionQuery(fusion="rrf"),
        limit=k,
    )

    retrieved_context_ids = []
    retrieved_context = []
    similarity_scores = []

    for result in results.points:
        retrieved_context_ids.append(result.payload["id"])
        retrieved_context.append(result.payload["vectorization_data"])
        similarity_scores.append(result.score)

    return {
        "retrieved_context_ids": retrieved_context_ids,
        "retrieved_context": retrieved_context,
        "similarity_scores": similarity_scores,
    }


@traceable(
    name="format_retrieved_context",
    run_type="prompt"
)
def process_context(context):

    formatted_context = ""

    for id, chunk in zip(
            context["retrieved_context_ids"], 
            context["retrieved_context"], 
        ):
        formatted_context += f"- ID: {id}, description: {chunk}\n"

    return formatted_context


@traceable(
    name="build_prompt",
    run_type="prompt"
)
def build_prompt(preprocessed_context, question):

    template = prompt_template_config("src/rag/prompts/retrieval_generation.yaml", "retrieval_generation")
    rendered_prompt = template.render(preprocessed_context=preprocessed_context, question=question)

    return rendered_prompt


@traceable(
    name="generate_answer",
    run_type="llm",
    metadata={"ls_provider": "openai", "ls_model_name": "gpt-4.1-mini"}
)
def generate_answer(prompt):

    client = instructor.from_openai(openai.OpenAI())

    response, raw_response = client.chat.completions.create_with_completion(
        model="gpt-4.1-mini",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.5,
        response_model=RAGGenerationResponseWithReferences
    )

    current_run = get_current_run_tree()

    if current_run:
        current_run.metadata["usage_metadata"] = {
            "input_tokens": raw_response.usage.prompt_tokens,
            "output_tokens": raw_response.usage.completion_tokens,
            "total_tokens": raw_response.usage.total_tokens
        }

    return response


@traceable(
    name="rag_pipeline"
)
def rag_pipeline(question, qdrant_client, top_k=5):

    retrieved_context = retrieve_data(question, qdrant_client, top_k)
    preprocessed_context = process_context(retrieved_context)
    prompt = build_prompt(preprocessed_context, question)
    answer = generate_answer(prompt)

    final_result = {
        "answer": answer.answer,
        "references": answer.references,
        "question": question,
        "retrieved_context_ids": retrieved_context["retrieved_context_ids"],
        "retrieved_context": retrieved_context["retrieved_context"],
        "similarity_scores": retrieved_context["similarity_scores"]
    }

    return final_result


def rag_pipeline_wrapper(question, top_k=5):
    
    # Use Qdrant Cloud in production, local in development
    if config.QDRANT_API_KEY:
        qdrant_client = QdrantClient(
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY
        )
    else:
        qdrant_client = QdrantClient(url="http://qdrant:6333")

    result = rag_pipeline(question, qdrant_client, top_k)

    used_context = []
    dummy_vector = np.zeros(1536).tolist()

    # that part if only useful to fetch non-vectorized data
    # such as attester address
    # this could be removed as we don't return attester address in the response
    for item in result.get("references", []):
        payload = qdrant_client.query_points(
            collection_name="Hackathon-attestation-collection-01-hybrid-search",
            query=dummy_vector,
            using="text-embedding-3-small",
            limit=1,
            with_payload=True,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="id", 
                        match=MatchValue(value=item.id))
                ]
            )
        ).points[0].payload
        attester = payload.get("attester")
        if attester:
            used_context.append({"attester": attester, "project_link": item.project_link, "project_description": item.project_description})

    return {
        "answer": result["answer"],
        "used_context": used_context
    }

def retrieve_context_wrapper(query, top_k=5):
    
    # Use Qdrant Cloud in production, local in development
    if config.QDRANT_API_KEY:
        qdrant_client = QdrantClient(
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY
        )
    else:
        qdrant_client = QdrantClient(url="http://qdrant:6333")

    return retrieve_data(query, qdrant_client, top_k)