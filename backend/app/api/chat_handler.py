# backend/app/api/chat_handler.py
import os

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser
from typing import Dict, Optional
import faiss
from ..utils.logger import logger
from ..utils.file_handler import load_markdown_files, save_vectorstore, load_vectorstore
from ..utils.text_processor import clean_text, format_api_response
from ..config import (
    VECTOR_STORE_DIR,
    MODEL_SETTINGS,
    VECTOR_STORE_SETTINGS
)


class ChatHandler:
    def __init__(self):
        logger.info("Initializing ChatHandler")

        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        self.vectorstore = self.initialize_vectorstore()
        self.llm = ChatOpenAI(
            model_name=MODEL_SETTINGS["chat_model"],
            temperature=MODEL_SETTINGS["temperature"]
        )
        self.retrieval_chain = self.create_retrieval_chain()
        logger.info("ChatHandler initialized successfully")

    def create_retrieval_chain(self):
        """Create the RAG retrieval chain"""
        # Configure retriever to get top k most similar chunks
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 3}  # Get top 3 most relevant chunks
        )

        # Create the prompt template that will be used with retrieved chunks
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Use the following pieces of API documentation to answer the user's question.
                          Always provide code examples when available in the documentation.
                          If specific information isn't found in the context, say that you don't have that specific information in the documentation.
                          Format API examples using markdown code blocks.

            Context: {context}"""),
            ("user", "{question}")
        ])

        # Create the chain that:
        # 1. Takes user's question
        # 2. Retrieves relevant docs
        # 3. Formats prompt with context
        # 4. Gets LLM completion
        chain = (
                {
                    "context": retriever,  # Retrieve relevant docs
                    "question": RunnablePassthrough()  # Pass the original question
                }
                | prompt  # Format the prompt with context and question
                | self.llm  # Get completion from LLM
                | StrOutputParser()  # Convert to string
        )

        return chain

    def initialize_vectorstore(self):
        """Initialize or load FAISS vectorstore"""
        # Try to load existing vectorstore
        vectorstore = load_vectorstore(VECTOR_STORE_DIR, self.embeddings)
        if vectorstore:
            logger.info("Loaded existing vector store")
            return vectorstore

        # If not found, create new vectorstore
        logger.info("Creating new vector store")
        docs = load_markdown_files()

        # Split documents
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "header1"),
                ("##", "header2"),
                ("###", "header3"),
            ]
        )

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=VECTOR_STORE_SETTINGS["chunk_size"],
            chunk_overlap=VECTOR_STORE_SETTINGS["chunk_overlap"]
        )

        all_splits = []
        for doc_name, content in docs.items():
            logger.info(f"Processing document: {doc_name}")
            header_splits = markdown_splitter.split_text(content)
            splits = text_splitter.split_documents(header_splits)
            all_splits.extend(splits)
            logger.info(f"Created {len(splits)} chunks from {doc_name}")

        # Create FAISS index
        sample_embedding = self.embeddings.embed_query("sample text")
        index = faiss.IndexFlatL2(len(sample_embedding))

        # Create vectorstore
        vectorstore = FAISS(
            embedding_function=self.embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )

        # Add documents to vectorstore
        if all_splits:
            vectorstore.add_documents(all_splits)
            logger.info(f"Added {len(all_splits)} documents to vector store")

        # Save for future use
        save_vectorstore(vectorstore, VECTOR_STORE_DIR)
        logger.info("Vector store created and saved")

        return vectorstore

    async def get_response(self, message: str, conversation_id: Optional[str] = None) -> Dict:
        """Process user message and return response"""
        try:
            logger.info(f"Processing message: {message[:50]}...")

            # Clean the input text
            cleaned_message = clean_text(message)

            # Get response from the RAG chain
            raw_response = self.retrieval_chain.invoke(cleaned_message)

            # Format the response
            formatted_response = format_api_response(raw_response)

            logger.info("Successfully generated response")

            return {
                "response": formatted_response,
                "conversation_id": conversation_id
            }

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "response": "I apologize, but I encountered an error. Please try again.",
                "conversation_id": conversation_id,
                "error": str(e)
            }
