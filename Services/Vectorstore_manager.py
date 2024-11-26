import numpy as np
from typing import List, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
import bs4
from langchain.text_splitter import RecursiveCharacterTextSplitter

class VectorStoreManager:
    def __init__(self):
        self.vector_store = None

    def create_vector_store(
        self,
        documents: List,
        embeddings: HuggingFaceEmbeddings
    ) -> Optional[FAISS]:
        """Create FAISS vector store from documents"""
        if not embeddings:
            raise ValueError("Embeddings are empty")
        
        try:
            self.vector_store = FAISS.from_documents(documents, embeddings)
            return self.vector_store
        except Exception as e:
            print(f"Error creating vector store: {str(e)}")
            return None

    def save_vector_store(self, path: str):
        """Save vector store to disk"""
        if self.vector_store:
            self.vector_store.save_local(path)