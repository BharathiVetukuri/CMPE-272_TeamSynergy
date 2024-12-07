from typing import List, Tuple
from .llm_service import RAGService


async def query_vector_store( queries: List[str]) -> List[dict]:
    """
    Load vector store and perform queries
    
    Args:
        save_path: Path to the saved vector store
        queries: List of queries to process
        
    Returns:
        List[dict]: List of query results
    """
    try:
        # Initialize RAG service and load vector store
        rag_service = RAGService(
         
        )
   
        
        # Process queries and collect results
        results = []
        for query in queries:
            print(f"\nProcessing query: {query}")
            try:
                result = await rag_service.get_answer(query)
                print(f"Result: {result}")
                results.append({
                    "query": query,
                    "success": True,
                    "result": {"answer": result}  
                })
                return results
            except Exception as e:
                results.append({
                    "query": query,
                    "success": False,
                    "error": str(e)
                })
                
        return results
    except Exception as e:
        print(f"Error in query_vector_store: {str(e)}")
        return []