import os
import glob
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

# Initialize ChromaDB Client
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

# Initialize Nomic Embeddings locally (free, open source)
try:
    embeddings = HuggingFaceEmbeddings(
        model_name="nomic-ai/nomic-embed-text-v1.5",
        model_kwargs={'trust_remote_code': True}
    )
except Exception as e:
    print(f"Error loading embeddings: {e}")
    embeddings = None

# Get or create collection
collection = chroma_client.get_or_create_collection(name="vwo_docs")

class QueryRequest(BaseModel):
    question: str
    groq_api_key: str

@app.post("/ingest")
async def ingest_documents():
    """Reads PDFs and DOCX files from the data folder, chunks them, and stores in ChromaDB"""
    if not embeddings:
        raise HTTPException(status_code=500, detail="Embeddings model not loaded properly.")
    
    pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
    docx_files = glob.glob(os.path.join(DATA_DIR, "*.docx"))
    all_files = pdf_files + docx_files
    
    if not all_files:
        raise HTTPException(status_code=404, detail="No PDF or DOCX files found in the 'data' folder. Please add a document.")
    
    all_chunks = []
    
    # Text splitter config
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    for file_path in all_files:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        else:
            loader = Docx2txtLoader(file_path)
            
        docs = loader.load()
        chunks = text_splitter.split_documents(docs)
        
        for i, chunk in enumerate(chunks):
            chunk.metadata["source"] = os.path.basename(file_path)
            chunk.metadata["chunk_id"] = f"{os.path.basename(file_path)}_chunk_{i}"
            all_chunks.append(chunk)
            
    if not all_chunks:
        return {"message": "No text found in PDFs to chunk."}
        
    # Prepare data for ChromaDB
    documents = [chunk.page_content for chunk in all_chunks]
    metadatas = [chunk.metadata for chunk in all_chunks]
    ids = [chunk.metadata["chunk_id"] for chunk in all_chunks]
    
    # Generate embeddings
    embeds = embeddings.embed_documents(documents)
    
    # Store in ChromaDB
    collection.upsert(
        documents=documents,
        embeddings=embeds,
        metadatas=metadatas,
        ids=ids
    )
    
    return {
        "message": "Ingestion successful!", 
        "total_chunks_stored": len(all_chunks),
        "files_processed": [os.path.basename(f) for f in all_files]
    }

@app.get("/database")
async def get_database():
    """Returns all chunks stored in ChromaDB to display in the UI"""
    results = collection.get()
    return {
        "ids": results.get("ids", []),
        "documents": results.get("documents", []),
        "metadatas": results.get("metadatas", [])
    }

@app.post("/query")
async def query_rag(request: QueryRequest):
    """Retrieves relevant chunks and generates an answer using Groq"""
    if not request.groq_api_key:
        raise HTTPException(status_code=400, detail="Groq API key is required.")
        
    # Generate embedding for the question
    question_embedding = embeddings.embed_query(request.question)
    
    # Query ChromaDB (Top 3 chunks)
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )
    
    retrieved_chunks = results["documents"][0]
    retrieved_metadatas = results["metadatas"][0]
    retrieved_ids = results["ids"][0]
    
    # Combine chunks into context
    context = "\n\n".join([f"Chunk ID: {retrieved_ids[i]}\n{doc}" for i, doc in enumerate(retrieved_chunks)])
    
    # Call Groq API
    client = Groq(api_key=request.groq_api_key)
    
    system_prompt = (
        "You are a helpful assistant answering questions based on the provided context. "
        "If the answer is not in the context, say 'I cannot answer this based on the provided documents.'\n\n"
        f"Context:\n{context}"
    )
    
    try:
        # Using LLaMA 3.1 8B (equivalent to the open GPT model requested)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.question}
            ],
            model="llama-3.1-8b-instant", 
            temperature=0.2,
        )
        answer = chat_completion.choices[0].message.content
        
        return {
            "answer": answer,
            "retrieved_chunks": [
                {"id": retrieved_ids[i], "content": retrieved_chunks[i], "metadata": retrieved_metadatas[i]}
                for i in range(len(retrieved_chunks))
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
