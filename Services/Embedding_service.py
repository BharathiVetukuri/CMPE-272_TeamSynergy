import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
import bs4
from typing import List, Tuple
from Vectorstore_manager import VectorStoreManager
import asyncio
from langchain.schema import Document
from llm_service import RAGService

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
        dummy_docs = [
            Document(
                page_content="""Artificial Intelligence (AI) is revolutionizing healthcare. 
                Recent studies show that AI-powered diagnostic tools can detect diseases 
                with 95% accuracy. Medical professionals are increasingly adopting these 
                technologies to improve patient care and treatment outcomes. However, 
                experts warn about the importance of maintaining human oversight in 
                critical medical decisions.""",
                metadata={'source': 'https://example.com/ai-healthcare-article'}
            ),
            Document(
                page_content="""The global climate crisis demands immediate action. 
                Scientists report that renewable energy adoption has increased by 40% 
                in the past year. Solar and wind power installations are breaking records, 
                while costs continue to decrease. Governments worldwide are setting 
                ambitious targets for carbon neutrality by 2050.""",
                metadata={'source': 'https://example.com/climate-article'}
            ),
            Document(
                page_content="""Space exploration enters a new era with private companies 
                leading the charge. SpaceX and Blue Origin are developing reusable rocket 
                technology, significantly reducing launch costs. Plans for Mars colonization 
                are becoming more concrete, with the first human missions planned for the 
                2030s.""",
                metadata={'source': 'https://example.com/space-article'}
            )
        ]
        print("Using dummy data for testing")
        return dummy_docs


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
        print(f"Sample embedding of a document chunk: {sample_embedding}")
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



async def process_data(urls: List[str], save_path: str, status_placeholder=None):
    try:
        # Initialize components
        web_loader = WebDataLoader()
        embedding_manager = EmbeddingManager()
        chunk_splitter = DataChunkSplitter()
        vector_store_manager = VectorStoreManager()

        # Load data from URLs
        # data = web_loader.load_from_urls(urls, status_placeholder)
        data = web_loader.get_dummy_data()
        print(f"Data loaded from URLs are: {data}")

        # Get embeddings
        embeddings = embedding_manager.get_embeddings()

        # Split data into chunks
        splitted_docs, sample_embedding = chunk_splitter.split_data_chunks(
            data,
            embeddings
        )

        # Create and save vector store
        vector_store = vector_store_manager.create_vector_store(
            splitted_docs,
            embeddings
        )
        if vector_store:
            vector_store_manager.save_vector_store(save_path)
            return True
        return False

    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return False




async def main():
    # Step 1: Process and store embeddings
    urls = ["https://www.axios.com/2024/11/26/ozempic-medicare-medicaid-weight-loss-drugs"]
    save_path = "faiss_store"
    
    # Process the data and create vector store
    success = await process_data(urls, save_path)
    if not success:
        print("Failed to process and store embeddings")
        return

    # Step 2: Initialize RAG service and load vector store
    rag_service = RAGService(
        vector_store_path=save_path,
        embedding_model_name=MODEL_NAME  # Pass the same model name to RAGService
    )
    if not rag_service.load_vector_store():
        print("Failed to load vector store")
        return
    print("Vector store loaded successfully")

    # Step 3: Test some queries
    test_queries = [
        "What are the main topics discussed in the articles?",
        "What are the key findings about healthcare?",
        "What are the recent developments mentioned?"
    ]

    # Process each query
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            result = await rag_service.get_answer(query)
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print(f"Answer: {result['answer']}")
        except Exception as e:
            print(f"Error processing query: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())