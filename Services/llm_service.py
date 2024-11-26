from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os


class RAGService:
    def __init__(
        self,
        vector_store_path: str,
        embedding_model_name: str = "sentence-transformers/all-MiniLM-l6-v2"
    ):
        self.vector_store_path = vector_store_path
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": False}
        )
        load_dotenv()
      
        self.llm = self._initialize_llm()
        self.prompt = self._create_prompt()
        # self.embeddings = self._initialize_embeddings()
        self.vector_store = None
        self.retriever = None
        self.document_chain = None
        self.retrieval_chain = None

    def _initialize_llm(self):
        """Initialize the Groq LLM"""
        groq_api_key = os.environ.get("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        return ChatGroq(groq_api_key=groq_api_key, model_name="llama3-8b-8192")

    def _initialize_embeddings(self):
        """Initialize HuggingFace embeddings"""
        return HuggingFaceEmbeddings()

    def _create_prompt(self):
        """Create the prompt template"""
        template = """Use the following pieces of context to answer the question at the end. Please follow these rules:
        1. If the context doesn't contain enough information to answer the question directly, say "I don't have enough information to provide a complete answer, but here's what I found:" and then summarize the relevant details from the context.
        2. If you find relevant information in the context, provide a concise answer using a few sentences at most. Be confident in your response if the information is clearly stated in the context.
        3. Always include any specific examples or projects mentioned in the context that are relevant to the question.
        4. If there are relevant links or sources mentioned in the context, include them at the end of your answer.

        {context}

        Question: {input}

        Helpful Answer:"""
        return PromptTemplate(template=template, input_variables=["input", "context"])

    def load_vector_store(self):
        """Load the FAISS vector store from local storage"""
        try:
            self.vector_store = FAISS.load_local(
                self.vector_store_path,
                embeddings=self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"Dimension of loaded FAISS: {self.vector_store.index.d}")
            print("Vector store loaded successfully from file.")
            
            # Initialize retriever
            self.retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )
            
            # Initialize chains
            self.document_chain = create_stuff_documents_chain(self.llm, self.prompt)
            self.retrieval_chain = create_retrieval_chain(self.retriever, self.document_chain)
            
            return True
        except Exception as e:
            print(f"Error loading vector store: {str(e)}")
            return False

    async def get_answer(self, query: str):
        """Get answer for the given query"""
        if not self.retrieval_chain:
            raise ValueError("Vector store and chains not initialized. Call load_vector_store first.")
        
        try:
            result = self.retrieval_chain.invoke({"input": query})
            return result
        except Exception as e:
            print(f"Error getting answer: {str(e)}")
            return {"error": str(e)}