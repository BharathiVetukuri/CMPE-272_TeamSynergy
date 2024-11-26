import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
import bs4
from typing import List, Tuple

from langchain.schema import Document
from .Vectorstore_manager import VectorStoreManager
# from Vectorstore_manager import VectorStoreManager
from .llm_service import RAGService
# from llm_service import RAGService
import json

import os
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

class WebDataLoader:
    def __init__(self, class_names: tuple = ("group", "ArticleHeader-headline")):
        self.class_names = class_names

    def load_from_urls(self, urls: List[str], status_placeholder=None) -> List:
        """Load data from URLs using WebBaseLoader"""
        loader = WebBaseLoader(
            web_paths=urls,
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(class_=self.class_names)
            )
        )
        


    # [Document(metadata={'source': 'https://www.axios.com/2024/11/26/ozempic-medicare-medicaid-weight-loss-drugs'}, page_content='')] 
        print(f"Initialized WebLoader: {loader}")
        
        
        return loader.load()
    

    def get_dummy_data(self) -> List[Document]:
        """Return dummy documents for testing"""
        try:
            with open(r"D:\project\finallevelprojects\Uni_Assist\updated_data.json", 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                
            documents = []
            for item in json_data:
                # Only create Document if page_content is not empty
                if item.get('page_content'):
                    doc = Document(
                        page_content=item['page_content'],
                        metadata={
                            'source': item['metadata'].get('source', 'unknown'),
                            'title': item['metadata'].get('title', ''),
                            'language': item['metadata'].get('language', 'en')
                        }
                    )
                    documents.append(doc)
            
            if not documents:
                raise ValueError("No valid documents found in JSON file")
                
            print(f"Successfully loaded {len(documents)} documents from JSON file")
            return documents
            
        except Exception as e:
            print(f"Error loading JSON data: {str(e)}")
            # Return dummy document in case of error
            return [Document(
                page_content="Error loading data. This is a fallback document.",
                metadata={'source': 'error_fallback'}
            )]


class DataChunkSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
        separators: List[str] = ["\n\n", "\n", ".", ","]
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def split_data_chunks(
        self,
        data: List,
        embeddings: HuggingFaceEmbeddings
    ) -> Tuple[List, np.ndarray]:
        """Split documents and create sample embedding"""
        splitted_docs = self.text_splitter.split_documents(data)
        print(f"Splitted chunks are: {splitted_docs}")

        # Create sample embedding
        sample_embedding = np.array(
            embeddings.embed_query(splitted_docs[0].page_content)
        )
        # print(f"Sample embedding of a document chunk: {sample_embedding}")
        print(f"Size of the embedding: {sample_embedding.shape}")

        return splitted_docs, sample_embedding

MODEL_NAME = "sentence-transformers/all-MiniLM-l6-v2"
class EmbeddingManager:
    def __init__(
        self,
        model_name: str = MODEL_NAME,
        device: str = "cpu",
        normalize_embeddings: bool = False
    ):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": device},
            encode_kwargs={"normalize_embeddings": normalize_embeddings}
        )
    
    def get_embeddings(self):
        """Return the initialized embeddings object"""
        return self.embeddings



async def process_data(save_path: str):
    try:
        # Initialize components
        web_loader = WebDataLoader()
        embedding_manager = EmbeddingManager()
        chunk_splitter = DataChunkSplitter()
        vector_store_manager = VectorStoreManager()

        # Load data from URLs
        # data = web_loader.load_from_urls(urls, status_placeholder)
        data = web_loader.get_dummy_data()
        # print(f"Data loaded from URLs are: {data}")

        # Get embeddings
        embeddings = embedding_manager.get_embeddings()

        # Split data into chunks
        splitted_docs, sample_embedding = chunk_splitter.split_data_chunks(
            data,
            embeddings
        )

        print("Data chunks are splitted")

        # Create and save vector store
        vector_store = vector_store_manager.create_vector_store(
            splitted_docs,
            embeddings
        )
        if vector_store:
            vector_store_manager.save_vector_store(save_path)
            print("Vector store created and saved successfully")
            return True
        return False

    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return False



async def query_vector_store(save_path: str, queries: List[str]) -> List[dict]:
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
            vector_store_path=save_path,
            embedding_model_name=MODEL_NAME
        )
        
        if not rag_service.load_vector_store():
            raise Exception("Failed to load vector store")
        
        print("Vector store loaded successfully")
        
        # Process queries and collect results
        results = []
        for query in queries:
            print(f"\nProcessing query: {query}")
            try:
                result = await rag_service.get_answer(query)
                results.append({
                    "query": query,
                    "success": True,
                    "result": result
                })
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


# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(process_data("faiss_store"))