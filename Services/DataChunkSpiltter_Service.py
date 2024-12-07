import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Tuple
from pinecone.grpc import PineconeGRPC as Pinecone


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
        self.pc = Pinecone(api_key="pcsk_6Mu8XH_HUK11sy9HDDnLLKiJcJwjAfZWTYqhtJUSaL6sLuBFTX8fsvcTLh2y7uGQUVacSc")

    def split_data_chunks(
        self,
        data: List,
    ) -> Tuple[List, np.ndarray]:
        """Split documents and create sample embedding"""
        splitted_docs = self.text_splitter.split_documents(data)
        print(f"Splitted chunks are: {len(splitted_docs)}")

       # Create sample embedding
        sample_texts = [doc.page_content for doc in splitted_docs[:5]]  # Take first 5 chunks as a sample
        sample_embedding = self.pc.inference.embed(
            model="multilingual-e5-large",
            inputs=sample_texts,
            parameters={"input_type": "passage", "truncate": "END"}
        )
        print(f"Size of the embedding: {sample_embedding}")
        

        return splitted_docs, sample_embedding