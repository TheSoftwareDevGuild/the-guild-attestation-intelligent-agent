#!/usr/bin/env python3
"""
Script to upload data to Qdrant Cloud for production deployment.
This script should be run locally to populate your Qdrant Cloud instance.
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, Document, Modifier, VectorParams, PointStruct, SparseVectorParams, PayloadSchemaType
import openai
from dotenv import load_dotenv

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

def get_embedding(text, model="text-embedding-3-small"):
    """Get embedding for text using OpenAI API"""
    response = openai.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

def get_embeddings_batch(text_list, model="text-embedding-3-small", batch_size=100):
    
    if len(text_list) <= batch_size:
        response = openai.embeddings.create(input=text_list, model=model)
        return [embedding.embedding for embedding in response.data]
    
    all_embeddings = []
    counter = 1
    for i in range(0, len(text_list), batch_size):
        batch = text_list[i:i + batch_size]
        response = openai.embeddings.create(input=batch, model=model)
        all_embeddings.extend([embedding.embedding for embedding in response.data])
        print(f"Processed {counter * batch_size} of {len(text_list)}")
        counter += 1
    
    return all_embeddings

def upload_data_to_qdrant():
    """Upload data to Qdrant Cloud"""
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not all([qdrant_url, qdrant_api_key, openai_api_key]):
        print("❌ Missing required environment variables:")
        print("   - QDRANT_URL")
        print("   - QDRANT_API_KEY") 
        print("   - OPENAI_API_KEY")
        return False
    
    # Set OpenAI API key
    openai.api_key = openai_api_key
    
    # Initialize Qdrant client
    qdrant_client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key
    )
    
    # Collection name
    collection_name = "Hackathon-attestation-collection-01-hybrid-search"
    
    print(f"🔗 Connected to Qdrant Cloud: {qdrant_url}")
    
    # Load data
    data_path = Path(__file__).parent.parent / "data" / "eas_attestations" / "processed_devfolio_attestations_for_vectorization.jsonl"
    
    if not data_path.exists():
        print(f"❌ Data file not found: {data_path}")
        return False
    
    print(f"📁 Loading data from: {data_path}")
    data_to_embed = pd.read_json(data_path, lines=True)
    data_to_embed = data_to_embed.to_dict(orient="records")
    print(f"📊 Loaded {len(data_to_embed)} records")
    
    # Create collection if it doesn't exist
    try:
        qdrant_client.get_collection(collection_name)
        print(f"✅ Collection '{collection_name}' already exists")
    except:
        print(f"🆕 Creating collection '{collection_name}'")
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config={"text-embedding-3-small": VectorParams(size=1536, distance=Distance.COSINE)},
            sparse_vectors_config={"bm25": SparseVectorParams(modifier=Modifier.IDF)}
        )
        qdrant_client.create_payload_index(
            collection_name=collection_name,
            field_name="id",
            field_schema=PayloadSchemaType.KEYWORD
        )
    
    # Process and upload data in batches
    batch_size = 100
    pointstructs = []
    
    print("🔄 Processing and embedding data...")
    # for i, data in enumerate(data_to_embed):
    #     if i % 50 == 0:
    #         print(f"   Processed {i}/{len(data_to_embed)} records")
        
    #     try:
    #         embedding = get_embedding(data["vectorization_data"])
    #         pointstructs.append(
    #             PointStruct(
    #                 id=i,
    #                 vector=embedding,
    #                 payload=data
    #             )
    #         )
    #     except Exception as e:
    #         print(f"⚠️  Error processing record {i}: {e}")
    #         continue
    text_to_embed = [data["vectorization_data"] for data in data_to_embed]
    embeddings = get_embeddings_batch(text_to_embed)
    pointstructs = []
    i = 1
    for embedding, data in zip(embeddings, data_to_embed):
        pointstructs.append(
            PointStruct(
                id=i,
                vector={
                    "text-embedding-3-small": embedding,
                    "bm25": Document(
                        text=data["vectorization_data"],
                        model="qdrant/bm25"
                    )
                },
                payload=data
            )
        )
        i += 1
        
    print(f"📤 Uploading {len(pointstructs)} points to Qdrant Cloud...")
    
    # Upload in batches
    for i in range(0, len(pointstructs), batch_size):
        batch = pointstructs[i:i+batch_size]
        qdrant_client.upsert(
            collection_name=collection_name,
            wait=True,
            points=batch
        )
        print(f"   Uploaded batch {i//batch_size + 1}/{(len(pointstructs)-1)//batch_size + 1}")
    
    print("✅ Data upload completed successfully!")
    
    # Verify upload
    collection_info = qdrant_client.get_collection(collection_name)
    print(f"📈 Collection now contains {collection_info.points_count} points")
    
    return True

if __name__ == "__main__":
    success = upload_data_to_qdrant()
    sys.exit(0 if success else 1)
