import os
from typing import List, Optional

# LangChain Imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Groq Import
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PDFQAAgent:
    def __init__(self):
        # Initialize Embeddings (using a lightweight, high-performance model)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize Groq Client
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=api_key)
        
        # Initialize Vector Store placeholder
        self.vectorstore = None

    def load_pdf(self, file_path: str) -> int:
        """
        Loads a PDF, splits it into chunks, and creates a vector store.
        Returns the number of chunks created.
        """
        # 1. Load PDF
        loader = PyPDFLoader(file_path)
        pages = loader.load()

        # 2. Split Text
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = splitter.split_documents(pages)

        # 3. Create or Update FAISS Vector Store
        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(
                documents=chunks,
                embedding=self.embeddings,
            )
        else:
            self.vectorstore.add_documents(documents=chunks)
        
        return len(chunks)

    def ask(self, question: str) -> str:
        """
        Retrieves relevant context and asks the LLM.
        """
        if not self.vectorstore:
            # General Chat Mode (No PDF loaded)
            context = ""
            system_prompt = "You are a helpful assistant. Answer the user's question to the best of your ability."
        else:
            # RAG Mode (PDF loaded)
            relevant_docs = self.vectorstore.similarity_search(question, k=3)
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            system_prompt = "You are a helpful and accurate assistant. Answer the user's question using the provided context. If the context is not relevant to the question, answer from your general knowledge."
        
        user_message = f"""Context:
{context}

Question: 
{question}
"""

        # 3. Call Groq LLM
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0,
                max_tokens=1024,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error communicating with AI: {str(e)}"