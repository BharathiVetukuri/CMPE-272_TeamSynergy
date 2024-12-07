from fastapi import FastAPI
import uvicorn
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
import os
from fastapi import HTTPException
from typing import Optional
from Services.QueryProcessingService import query_vector_store
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from your local React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
def connect_db():
    client = MongoClient(os.environ["MONGO_DB_KEY"])
    db = client["synergy_db"]
    return db



#DataModel

class QueryRequest(BaseModel):
    queries: List[str]

class QueryResponse(BaseModel):
    query: str
    success: bool
    result: Optional[dict] = None
    error: Optional[str] = None

@app.post("/query/", response_model=List[QueryResponse])
async def query_documents(request: QueryRequest):
    """
    Process queries against the vector store
    
    Args:
        request: QueryRequest containing list of queries
        
    Returns:
        List[QueryResponse]: Results for each query
    """
    try:
        # Path to your vector store - you might want to make this configurable
        # save_path = "./Services/faiss_store"
        
        # Check if vector store exists
        # if not os.path.exists(save_path):
        #     raise HTTPException(
        #         status_code=404,
        #         detail="Vector store not found. Please ensure documents are embedded first."
        #     )
        
        # Process queries
        results = await query_vector_store( request.queries)
        
        # Format results for API response
        formatted_results = []
        for result in results:
            formatted_results.append(QueryResponse(
                query=result["query"],
                success=result["success"],
                result=result.get("result"),
                error=result.get("error")
            ))
        
        return formatted_results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)
