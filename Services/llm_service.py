from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from typing import List
from langchain.schema import BaseRetriever, Document
from .Vectorstore_manager import VectorStoreManager


    
class RAGService:
    def __init__(
        self,
       
    ):
      
        load_dotenv()
      
        self.llm = self._initialize_llm()
        self.prompt = self._create_prompt()
        self.vector_store_manager = VectorStoreManager()
      

    def _initialize_llm(self):
        """Initialize the Groq LLM"""
        groq_api_key = os.environ.get("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        return ChatGroq(groq_api_key=groq_api_key, model_name="llama3-8b-8192")


    def _create_prompt(self):
        """Create the prompt template"""
        template = """Use the following pieces of context to answer the question at the end. Please follow these rules:
        1. If the context doesn't contain enough information to answer the question directly, say "I don't have enough information to provide a complete answer, but here's what I found:" and then summarize the relevant details from the context.
        2. If you find relevant information in the context, provide a concise answer using a few sentences at most. Be confident in your response if the information is clearly stated in the context.
        3. Always include any specific examples or projects mentioned in the context that are relevant to the question.
        4. If there are relevant links or sources mentioned in the context, include them at the end of your answer.
        5. Also provide the source website urlwhere user can find more details.

        {context}

        Question: {input}

        Helpful Answer:"""
        return PromptTemplate(template=template, input_variables=["input", "context"])



    async def get_answer(self, query: str):
        """Get answer for the given query"""


        
        try:
            context = self.vector_store_manager.fetch_data(query)
            customchain = self.prompt | self.llm
            result = customchain.invoke({"input": query, "context":context, })
            print(f"Result1: {result}")
            # print(f"Result1: {result}")
            return result.content
        except Exception as e:
            print(f"Error getting answer: {str(e)}")
            return {"error": str(e)}