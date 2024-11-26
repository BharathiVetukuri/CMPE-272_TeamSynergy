import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
import bs4
from typing import List, Tuple
from Vectorstore_manager import VectorStoreManager
import asyncio

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

        dummy_data = [
            {
                'page_content': """
                Ozempic and weight loss drugs are transforming healthcare.
                Medicare and Medicaid are considering coverage options.
                Key points:
                """,
                'metadata': {'source': urls[0]}
            }
        ]
          

    # [Document(metadata={'source': 'https://www.axios.com/2024/11/26/ozempic-medicare-medicaid-weight-loss-drugs'}, page_content='')] 
        print(f"Initialized WebLoader: {loader}")
        
        if status_placeholder:
            status_placeholder.text("Data Loading...Started...✅✅✅")
        
        return loader.load()


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


class EmbeddingManager:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-l6-v2",
        device: str = "cpu",
        normalize_embeddings: bool = False
    ):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": device},
            encode_kwargs={"normalize_embeddings": normalize_embeddings}
        )

    def get_embeddings(self) -> HuggingFaceEmbeddings:
        return self.embeddings
    



async def process_data(urls: List[str], save_path: str, status_placeholder=None):
    try:
        # Initialize components
        web_loader = WebDataLoader()
        embedding_manager = EmbeddingManager()
        chunk_splitter = DataChunkSplitter()
        vector_store_manager = VectorStoreManager()

        # Load data from URLs
        data = web_loader.load_from_urls(urls, status_placeholder)
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

# Example usage
urls = ["https://www.axios.com/2024/11/26/ozempic-medicare-medicaid-weight-loss-drugs",]
save_path = "faiss_store"

success = asyncio.run(process_data(urls, save_path))
if success:
    print("Data processing completed successfully")
else:
    print("Data processing failed")