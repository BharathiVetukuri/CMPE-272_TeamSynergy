import numpy as np
from typing import List, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
import bs4
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from typing import List, Optional, Dict
import time


    
class VectorStoreManager:
    def __init__(self):
        self.pc = Pinecone(api_key="pcsk_6Mu8XH_HUK11sy9HDDnLLKiJcJwjAfZWTYqhtJUSaL6sLuBFTX8fsvcTLh2y7uGQUVacSc")
        self.index_name = "uniassist-vectorstore"

    def create_vector_store(
        self,
        documents: List,
        
    ) -> Optional[FAISS]:
        """Create FAISS vector store from documents"""
        if not documents:
            raise ValueError("Documents are empty")
        
        try:
            self.vector_store = FAISS.from_documents(documents, embeddings)
            if self.index_name:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1024,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
            index = self.pc.Index(self.index_name)
            
                      # Process documents in smaller batches
            batch_size = 50  # Adjust this value based on your needs
            for i in range(0, len(documents), batch_size):
                batch_documents = documents[i:i+batch_size]
                
                # Generate embeddings for the current batch
                embeddings = self.pc.inference.embed(
                    model="multilingual-e5-large",
                    inputs=[doc.page_content for doc in batch_documents],
                    parameters={"input_type": "passage", "truncate": "END"}
                )
                
                # Prepare data for upsert
                vectors_to_upsert = [
                    (f"{i+j}", embedding['values'], {"text": batch_documents[j].page_content})
                    for j, embedding in enumerate(embeddings)
                ]
                
                # Upsert the current batch
                index.upsert(vectors=vectors_to_upsert)
                
                print(f"Upserted batch {i//batch_size + 1} of {len(documents)//batch_size + 1}")
                
                # Add a small delay to avoid rate limiting
                time.sleep(1)
            
            return True
        except Exception as e:
            print(f"Error creating vector store: {str(e)}")
            return None
        
    def fetch_data(self, query: str, top_k: int = 5) -> List[Dict]:
        """Fetch data from vector store based on similarity to query"""
        try:
            index = self.pc.Index(self.index_name)
            
            # Embed the query
            query_embedding = self.pc.inference.embed(
                model="multilingual-e5-large",
                inputs=[query],
                parameters={
                    "input_type": "query"
                }
            )
            
            # Perform similarity search
            results = index.query(
                vector=query_embedding[0].values,
                top_k=top_k,
                include_metadata=True
            )
            
            # Extract and return the results
            return [
                {
                    "id": match.id,
                    "score": match.score,
                    "text": match.metadata["text"]
                }
                for match in results.matches
            ]
        except Exception as e:
            print(f"Error fetching data from vector store: {str(e)}")
            return []    

