import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
import bs4
from typing import List, Tuple
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain.schema import Document
from .Vectorstore_manager import VectorStoreManager
# from Vectorstore_manager import VectorStoreManager
from .llm_service import RAGService
# from llm_service import RAGService
from .DataChunkSpiltter_Service import DataChunkSplitter
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




# MODEL_NAME = "sentence-transformers/all-MiniLM-l6-v2"
# class EmbeddingManager:
#     def __init__(
#         self,
#         # model_name: str = MODEL_NAME,
#         device: str = "cpu",
#         normalize_embeddings: bool = False
#     ):
#         self.embeddings = HuggingFaceEmbeddings(
#             model_name=model_name,
#             model_kwargs={"device": device},
#             encode_kwargs={"normalize_embeddings": normalize_embeddings}
#         )
    
#     def get_embeddings(self):
#         """Return the initialized embeddings object"""
#         return self.embeddings



# async def process_data():
#     try:
#         # Initialize components
#         web_loader = WebDataLoader()
#         # embedding_manager = EmbeddingManager()
#         chunk_splitter = DataChunkSplitter()
#         vector_store_manager = VectorStoreManager()

#         # Load data from URLs
#         # url = "https://www.sjsu.edu/"
#         # data = web_loader.load_from_urls(url)
#         data = web_loader.get_dummy_data()
#         print(f"Data loaded from URLs are: {len(data)}")

#          # Get embeddings
#         # embeddings = embedding_manager.get_embeddings()

#         # Split data into chunks
#         splitted_docs, sample_embedding = chunk_splitter.split_data_chunks(
#             data
#         )

#         print("Data chunks are splitted")

#         # Create and save vector store
#         vector_store = vector_store_manager.create_vector_store(
#             splitted_docs,
 
#         )
#         if vector_store:
#             print("Vector store created and data saved successfully")
#         else:
#             print("Failed to create vector store or save data")
       

#     except Exception as e:
#         print(f"Error processing data: {str(e)}")
#         return False






# if __name__ == "__main__":
#     import asyncio
    # asyncio.run(process_data())