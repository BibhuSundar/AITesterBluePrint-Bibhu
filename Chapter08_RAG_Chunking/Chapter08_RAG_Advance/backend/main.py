import os
import io
import json
import glob
import pandas as pd
import uuid
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Embedding and vector store
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Document loaders
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredExcelLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter, Language

# Reranker
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# LLM
from groq import Groq

app = FastAPI(title="Advanced RAG Explorer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
QDRANT_DIR = os.path.join(BASE_DIR, "qdrantStorage")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(QDRANT_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

# Global models
embeddings_model = None
reranker_model = None
reranker_tokenizer = None
qdrant_client = None

@dataclass
class ChunkInfo:
    chunk_id: str
    content: str
    source_file: str
    start_index: int
    end_index: int
    token_count: int
    chunk_size_chars: int

@dataclass
class IngestionResult:
    total_documents: int
    total_chunks: int
    chunk_size: int
    overlap: int
    chunks: List[ChunkInfo]
    vector_db_name: str
    embedding_model: str
    timestamp: str

@dataclass
class RetrievalResult:
    query: str
    initial_chunks_retrieved: int
    chunks_after_rerank: int
    reranker_model: str
    final_results: List[dict]
    llm_response: str
    metadata: dict

class QueryRequest(BaseModel):
    question: str
    groq_api_key: str
    top_k_initial: int = 10
    top_k_final: int = 5

class GenerateTCRequest(BaseModel):
    jira_id: str
    jira_domain: str
    jira_email: str
    jira_token: str
    groq_api_key: str
    output_format: str

def load_embedding_model():
    global embeddings_model
    try:
        embeddings_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs={'trust_remote_code': True}
        )
        print("BGE-M3 embeddings model loaded successfully!")
        return embeddings_model
    except Exception as e:
        print(f"Error with BGE-M3, falling back to nomic: {e}")
        embeddings_model = HuggingFaceEmbeddings(
            model_name="nomic-ai/nomic-embed-text-v1.5",
            model_kwargs={'trust_remote_code': True}
        )
        return embeddings_model

def load_reranker_model():
    global reranker_model, reranker_tokenizer
    try:
        reranker_tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-reranker-v2-m3")
        reranker_model = AutoModelForSequenceClassification.from_pretrained("BAAI/bge-reranker-v2-m3")
        reranker_model.eval()
        print("BGE Reranker model loaded successfully!")
        return reranker_model, reranker_tokenizer
    except Exception as e:
        print(f"Error loading reranker: {e}")
        return None, None

def init_qdrant():
    global qdrant_client
    try:
        qdrant_client = QdrantClient(path=QDRANT_DIR)
        collections = qdrant_client.get_collections()
        collection_names = [c.name for c in collections.collections]
        
        if "vwo_test_cases" not in collection_names:
            qdrant_client.create_collection(
                collection_name="vwo_test_cases",
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
            )
            print("Created Qdrant collection!")
        else:
            print("Qdrant collection already exists!")
        
        return qdrant_client
    except Exception as e:
        print(f"Error initializing Qdrant: {e}")
        return None

@app.on_event("startup")
async def startup_event():
    global embeddings_model, reranker_model, reranker_tokenizer, qdrant_client
    try:
        embeddings_model = load_embedding_model()
    except Exception as e:
        print(f"Could not load embeddings: {e}")
    
    try:
        reranker_model, reranker_tokenizer = load_reranker_model()
    except Exception as e:
        print(f"Could not load reranker: {e}")
    
    try:
        qdrant_client = init_qdrant()
    except Exception as e:
        print(f"Could not initialize Qdrant: {e}")

@app.get("/")
async def root():
    return {
        "message": "Advanced RAG Explorer API",
        "version": "1.0.0",
        "features": [
            "BGE-M3 Embeddings",
            "Qdrant Vector Database",
            "BGE Reranker v2",
            "Groq LLM Integration"
        ]
    }

@app.get("/status")
async def get_status():
    return {
        "embedding_model": "BAAI/bge-m3" if embeddings_model else "Not loaded",
        "reranker_model": "BAAI/bge-reranker-v2-m3" if reranker_model else "Not loaded",
        "vector_db": "Qdrant" if qdrant_client else "Not initialized",
        "qdrant_collections": qdrant_client.get_collections().collections if qdrant_client else []
    }

@app.post("/upload_preview")
async def upload_preview(file: UploadFile = File(...)):
    """Upload and preview how data will be chunked"""
    if not embeddings_model:
        raise HTTPException(status_code=500, detail="Embeddings model not loaded")
    
    # Read file content
    content = await file.read()
    file_name = file.filename
    extension = os.path.splitext(file_name)[1].lower()
    
    temp_path = os.path.join(DATA_DIR, f"temp_{file_name}")
    
    try:
        with open(temp_path, "wb") as f:
            f.write(content)
        
        # Determine loader
        if extension == '.csv':
            loader = CSVLoader(temp_path, encoding='utf-8')
            df = pd.read_csv(temp_path)
        elif extension == '.xlsx':
            loader = UnstructuredExcelLoader(temp_path)
            df = pd.read_excel(temp_path)
        elif extension == '.xls':
            loader = UnstructuredExcelLoader(temp_path)
            df = pd.read_excel(temp_path)
        elif extension == '.pdf':
            loader = PyPDFLoader(temp_path)
        elif extension == '.docx':
            loader = Docx2txtLoader(temp_path)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {extension}")
        
        # Load documents
        docs = loader.load()
        
        # Show raw data preview for structured files
        raw_data = []
        if extension in ['.csv', '.xlsx', '.xls']:
            raw_data = df.head(20).to_dict('records')
            total_rows = len(df)
        else:
            total_rows = len(docs)
        
        # Show chunking preview
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True
        )
        
        chunks = text_splitter.split_documents(docs)
        
        chunk_preview = []
        for i, chunk in enumerate(chunks[:10]):
            chunk_preview.append({
                "chunk_id": f"chunk_{i}",
                "content": chunk.page_content[:200] + "..." if len(chunk.page_content) > 200 else chunk.page_content,
                "content_length": len(chunk.page_content),
                "metadata": chunk.metadata
            })
        
        # Clean up
        os.remove(temp_path)
        
        return {
            "file_name": file_name,
            "file_type": extension,
            "total_records": total_rows,
            "raw_data_preview": raw_data[:5],
            "chunking_config": {
                "chunk_size": 500,
                "chunk_overlap": 100,
                "total_chunks": len(chunks)
            },
            "chunk_preview": chunk_preview,
            "embedding_model": "BAAI/bge-m3",
            "vector_dimension": 1024
        }
        
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/ingest")
async def ingest_documents(
    file: UploadFile = File(...),
    chunk_size: int = Form(500),
    chunk_overlap: int = Form(100),
    embedding_model: str = Form("BAAI/bge-m3")
):
    """Ingest documents with custom chunking parameters"""
    if not embeddings_model:
        raise HTTPException(status_code=500, detail="Embeddings model not loaded")
    
    if not qdrant_client:
        raise HTTPException(status_code=500, detail="Vector DB not initialized")
    
    content = await file.read()
    file_name = file.filename
    extension = os.path.splitext(file_name)[1].lower()
    
    temp_path = os.path.join(DATA_DIR, f"temp_{file_name}")
    
    try:
        with open(temp_path, "wb") as f:
            f.write(content)
        
        # Load and chunk
        if extension == '.csv':
            loader = CSVLoader(temp_path, encoding='utf-8')
        elif extension in ['.xlsx', '.xls']:
            loader = UnstructuredExcelLoader(temp_path)
        elif extension == '.pdf':
            loader = PyPDFLoader(temp_path)
        elif extension == '.docx':
            loader = Docx2txtLoader(temp_path)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type")
        
        docs = loader.load()
        
        # Create chunk splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True
        )
        
        chunks = text_splitter.split_documents(docs)
        
        # Generate embeddings in batch for faster processing
        print(f"Generating embeddings for {len(chunks)} chunks...")
        
        # Extract all texts for batch embedding
        texts = [chunk.page_content for chunk in chunks]
        
        # Use embed_documents for batch processing (much faster)
        embeddings = embeddings_model.embed_documents(texts)
        
        # Create points with embeddings
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "content": chunk.page_content,
                    "source_file": file_name,
                    "chunk_id": i,
                    "metadata": chunk.metadata
                }
            )
            points.append(point)
        
        print(f"Generated {len(points)} embeddings successfully!")
        
        # Store in Qdrant
        if points:
            qdrant_client.upsert(
                collection_name="vwo_test_cases",
                points=points
            )
        
        # Clean up
        os.remove(temp_path)
        
        return {
            "message": "Ingestion successful!",
            "total_documents": len(docs),
            "total_chunks": len(chunks),
            "chunks_stored": len(points),
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "embedding_model": embedding_model,
            "vector_db": "Qdrant",
            "file_name": file_name,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Ingestion error: {str(e)}")

@app.get("/database")
async def get_database(limit: int = 20):
    """Get stored chunks from vector database"""
    if not qdrant_client:
        raise HTTPException(status_code=500, detail="Vector DB not initialized")
    
    try:
        results = qdrant_client.scroll(
            collection_name="vwo_test_cases",
            limit=limit,
            with_payload=True
        )
        
        chunks = []
        for point in results[0]:
            chunks.append({
                "id": point.id,
                "content": point.payload.get("content", "")[:300] + "..." if len(point.payload.get("content", "")) > 300 else point.payload.get("content", ""),
                "source_file": point.payload.get("source_file", ""),
                "chunk_id": point.payload.get("chunk_id", 0)
            })
        
        total = qdrant_client.get_collection(collection_name="vwo_test_cases").points_count
        
        return {
            "total_chunks": total,
            "chunks": chunks
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching database: {str(e)}")

@app.post("/query")
async def query_rag(request: QueryRequest):
    """Query the RAG with retrieval and reranking visualization"""
    if not embeddings_model:
        raise HTTPException(status_code=500, detail="Embeddings model not loaded")
    
    if not qdrant_client:
        raise HTTPException(status_code=500, detail="Vector DB not initialized")
    
    try:
        # 1. Generate query embedding
        query_embedding = embeddings_model.embed_query(request.question)
        
        # 2. Initial retrieval from Qdrant
        search_results = qdrant_client.query_points(
            collection_name="vwo_test_cases",
            query=query_embedding,
            limit=request.top_k_initial
        )
        
        # Get points from query response
        if hasattr(search_results, 'result'):
            points = search_results.result
        elif hasattr(search_results, 'points'):
            points = search_results.points
        else:
            points = list(search_results)
        
        initial_chunks = []
        for point in points:
            if hasattr(point, 'payload'):
                payload = point.payload
                point_id = str(point.id)
                score = point.score
            else:
                payload = point if isinstance(point, dict) else {}
                point_id = str(point.id) if hasattr(point, 'id') else str(point[0]) if isinstance(point, tuple) else "unknown"
                score = point.score if hasattr(point, 'score') else (point[1] if isinstance(point, tuple) else 0.0)
            
            initial_chunks.append({
                "id": point_id,
                "content": payload.get("content", "") if isinstance(payload, dict) else "",
                "score": score,
                "source_file": payload.get("source_file", "") if isinstance(payload, dict) else ""
            })
        
        # 3. Reranking if reranker model loaded
        reranked_chunks = initial_chunks
        if reranker_model and reranker_tokenizer and len(initial_chunks) > 1:
            # Prepare query-document pairs for reranking
            pairs = [[request.question, chunk["content"]] for chunk in initial_chunks]
            
            inputs = reranker_tokenizer(pairs, padding=True, truncation=True, max_length=512, return_tensors="pt")
            
            with torch.no_grad():
                outputs = reranker_model(**inputs)
                scores = outputs.logits.squeeze()
            
            # Sort by reranker scores
            chunk_scores = []
            for i, chunk in enumerate(initial_chunks):
                score = scores[i].item() if len(scores) > 1 else scores.item()
                chunk_scores.append((score, chunk))
            
            chunk_scores.sort(key=lambda x: x[0], reverse=True)
            
            reranked_chunks = [chunk for _, chunk in chunk_scores[:request.top_k_final]]
        
        # 4. Generate LLM response
        context = "\n\n---\n\n".join([f"[Source: {chunk['source_file']}]\n{chunk['content']}" for chunk in reranked_chunks])
        
        client = Groq(api_key=request.groq_api_key)
        
        system_prompt = (
            f"You are an expert QA Assistant specializing in VWO (VWO Testing Platform). "
            f"Answer the user's question based ONLY on the provided context from test cases. "
            f"If the context doesn't contain enough information, say so clearly.\n\n"
            f"Context from test cases:\n{context}"
        )
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.question}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.2,
            max_tokens=2000
        )
        
        llm_response = chat_completion.choices[0].message.content
        
        return {
            "query": request.question,
            "retrieval_info": {
                "initial_chunks_retrieved": len(initial_chunks),
                "chunks_after_rerank": len(reranked_chunks),
                "reranker_model": "BAAI/bge-reranker-v2-m3" if reranker_model else "None"
            },
            "initial_chunks": initial_chunks[:request.top_k_initial],
            "reranked_chunks": reranked_chunks,
            "llm_response": llm_response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query error: {str(e)}")

@app.post("/generate_tc")
async def generate_test_cases(req: GenerateTCRequest):
    """Generate test cases from Jira issue"""
    import requests as req_lib
    
    jira_url = f"https://{req.jira_domain}.atlassian.net/rest/api/2/issue/{req.jira_id}"
    auth = (req.jira_email, req.jira_token)
    
    response = req_lib.get(jira_url, auth=auth, headers={"Accept": "application/json"})
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Failed to fetch Jira: {response.status_code}")
    
    issue_data = response.json()
    summary = issue_data.get("fields", {}).get("summary", "No Summary")
    description = issue_data.get("fields", {}).get("description", "No Description")
    
    client = Groq(api_key=req.groq_api_key)
    
    system_prompt = (
        "You are an expert QA Engineer. Generate comprehensive test cases for VWO platform. "
        "Cover functional, non-functional, edge cases, and boundary values. "
        "Return ONLY valid JSON array.\n"
        "Format: [{\"tc_id\": \"TC-01\", \"title\": \"Verify X\", \"steps\": \"1. Do A\\n2. Do B\", \"expected\": \"Result Y\"}]"
    )
    
    user_prompt = f"Jira: {req.jira_id}\nSummary: {summary}\nDescription: {description}"
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=2000
        )
        
        content = chat_completion.choices[0].message.content
        
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        tc_list = json.loads(content)
        
        return {
            "message": "Success",
            "jira_id": req.jira_id,
            "summary": summary,
            "test_cases": tc_list,
            "total_tc": len(tc_list)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get collection statistics"""
    if not qdrant_client:
        return {"message": "Qdrant not initialized"}
    
    try:
        collection = qdrant_client.get_collection(collection_name="vwo_test_cases")
        return {
            "collection_name": "vwo_test_cases",
            "total_points": collection.points_count,
            "vectors_size": collection.vectors_count,
            "status": collection.status
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)