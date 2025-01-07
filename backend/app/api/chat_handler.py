import json
import re
from typing import Dict, Optional

import faiss
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import Document
# --- IMPORT YOUR LOCAL MODULES/HELPERS ---
# Adjust these import paths based on your project structure:
from .conversation_handler import ConversationHandler  # The summarizing conversation handler
from ..utils.file_handler import load_markdown_files, save_vectorstore, load_vectorstore
from ..utils.logger import logger
from ..utils.text_processor import clean_text
from ..agents.crustdataagent import CrustDataAgent
from langchain.schema.runnable import RunnableLambda
from ..config import (
    VECTOR_STORE_DIR,
    MODEL_SETTINGS,
    VECTOR_STORE_SETTINGS,
    OPENAI_API_KEY  # if you store your key in config
)


# If you have an agent for API calls, you can import it here, e.g.:
# from agents.crustdataagent import CrustDataAgent


class ChatHandler:
    """
    Demonstration of a ChatHandler that:
      - Maintains summarized conversation history
      - Uses a vectorstore for RAG
      - Builds a prompt combining the conversation summary+recent messages and the RAG context
      - Sends to ChatOpenAI
    """

    def __init__(self):
        logger.info("Initializing ChatHandler")

        # 1) Embeddings & VectorStore
        self.embeddings = OpenAIEmbeddings(
            model=MODEL_SETTINGS["embedding_model"],
            openai_api_key=OPENAI_API_KEY
        )
        self.vectorstore = self.initialize_vectorstore()

        # 2) LLM (Chat Model)
        self.llm = ChatOpenAI(
            model_name=MODEL_SETTINGS["chat_model"],
            temperature=MODEL_SETTINGS["temperature"],
            openai_api_key=OPENAI_API_KEY
        )

        # 3) Conversation Handler (with Summaries)
        #    You might set a smaller or larger threshold for summarizing older messages
        self.conversation_handler = ConversationHandler(
            openai_api_key=OPENAI_API_KEY,
            max_messages_without_summary=6,  # e.g., summarize older messages after 6
            model_name="gpt-4o-mini"  # which model to use for summarizing
        )

        self.agent = CrustDataAgent(api_token="YOUR_API_TOKEN_HERE")

        # 5) Build our RAG retrieval chain
        self.retrieval_chain = self.create_retrieval_chain()

        logger.info("ChatHandler initialized successfully")

    from langchain.schema import Document  # <--- Make sure this import is at the top

    def initialize_vectorstore(self) -> FAISS:
        """
        Initialize or load a FAISS vectorstore.
        """
        # Try loading existing vectorstore
        vectorstore = load_vectorstore(VECTOR_STORE_DIR, self.embeddings)
        if vectorstore:
            logger.info("Loaded existing vectorstore from disk.")
            return vectorstore

        # If none exists, create a new one from your local markdown files:
        logger.info("No existing vectorstore found; creating a new one.")
        docs = load_markdown_files()  # Returns a dict {filename: content}

        # Simple text splitter (ignoring Markdown headers for brevity)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=VECTOR_STORE_SETTINGS["chunk_size"],
            chunk_overlap=VECTOR_STORE_SETTINGS["chunk_overlap"]
        )

        all_splits = []
        for doc_name, content in docs.items():
            logger.info(f"Processing document: {doc_name}")
            splits = text_splitter.split_text(content)
            # Store each chunk for further processing
            for chunk in splits:
                all_splits.append((doc_name, chunk))

        # Create FAISS index
        sample_embedding = self.embeddings.embed_query("test")
        index = faiss.IndexFlatL2(len(sample_embedding))
        vectorstore = FAISS(
            embedding_function=self.embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )

        # Build Document objects to add
        # Each chunk is now (doc_name, chunk_text), so we can store doc_name as metadata
        if all_splits:
            docs_to_add = [
                Document(
                    page_content=chunk_text,
                    metadata={"source": doc_name}
                )
                for (doc_name, chunk_text) in all_splits
            ]

            vectorstore.add_documents(docs_to_add)
            logger.info(f"Added {len(docs_to_add)} docs to vectorstore.")

        # Save for future usage
        save_vectorstore(vectorstore, VECTOR_STORE_DIR)
        logger.info("Vectorstore created and saved.")
        return vectorstore

    def create_retrieval_chain(self):
        """
        Create a retrieval chain that:
          - Retrieves top k relevant chunks
          - Merges them into a system prompt with placeholders
          - Runs them through the LLM
        """
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

        # Our prompt template for RAG
        # We'll fill {context} with the retrieved docs,
        # and {question} with the user query + conversation context.
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant with access to specific documentation.
        Use the documentation **verbatim** to provide an answer about searching for people (like current title, company, location).
        **If** the context mentions filter types or code examples, please include them in your response.
        If the info truly isn’t in the docs, say so.

        Context: {context}
        """),
            ("user", "{question}")
        ])

        logger.info("prompt:\n" + str(prompt))

        # Compose a chain:
        chain = (
                {
                    "context": retriever,
                    "question": RunnablePassthrough()
                }
                | self.log_docs_runnable  # <--- Insert logging step here
                | prompt
                | self.llm
                | StrOutputParser()
        )

        return chain

    async def get_response(self,
                           message: str,
                           conversation_id: str) -> Dict:
        """
        Main method to handle user messages:
          1) Store message in conversation (which may trigger summarization).
          2) Build a final prompt from:
             - Summaries + recent messages (ConversationHandler)
             - The user's new question
          3) Pass that combined "question" to the retrieval chain
          4) Run the agent on the LLM's answer to find/fix any API calls
          5) Return the (possibly updated) response
        """
        try:
            logger.info(f"New user message: {message[:50]}...")

            # 1. Clean and store user message
            cleaned = clean_text(message)
            self.conversation_handler.add_message(
                conversation_id=conversation_id,
                role="user",
                content=cleaned
            )
            logger.info(conversation_id)
            # 2. Build the conversation context (summary + recent messages)
            conversation_context = self.conversation_handler.get_context_for_llm(conversation_id)
            logger.info("added conversation context")

            # For RAG, combine conversation context and user question into a single prompt
            user_question = f"{conversation_context}\n\nNew question:\n{cleaned}"
            logger.info("Final prompt to LLM (truncated): " + user_question[:1500])

            # 3. Run the retrieval chain to get LLM's raw response
            response_text = await self.retrieval_chain.ainvoke(user_question)
            logger.info("response_text:" + response_text)

            # --- NEW STEP: Let the agent parse & fix API calls ---
            agent_result = await self.agent.process_message(
                message=response_text,
                conversation_id=conversation_id
            )

            if agent_result.get("agent_response"):
                # 1. Store the agent's message in the conversation (under 'agent' role)
                self.conversation_handler.add_agent_response(
                    conversation_id,
                    agent_result["agent_response"]
                )

                # 2. Append it to the LLM's original response
                combined_response = f"{response_text}\n\n---\n{agent_result['agent_response']}"
            else:
                combined_response = response_text

            # 4. Store the final “assistant” message in the conversation
            #    (This final message includes possible agent fixes.)
            self.conversation_handler.add_message(
                conversation_id=conversation_id,
                role="assistant",
                content=combined_response
            )

            # 5. Return response in a dict
            return {
                "response": combined_response,
                "conversation_id": conversation_id
            }

        except Exception as e:
            logger.error("Error in get_response:", exc_info=True)
            return {
                "response": f"An error occurred: {str(e)}",
                "conversation_id": conversation_id
            }

    def log_docs_step(inputs: dict) -> dict:
        """
        A small function that logs the docs from 'context'
        and returns the same inputs so the chain continues.
        """
        docs = inputs.get("context", [])
        logger.info("=== RAG Retrieved Documents ===")
        if isinstance(docs, list):
            for i, doc in enumerate(docs, start=1):
                logger.info(f"Doc #{i} metadata: {doc.metadata}")
                logger.info(f"Doc #{i} content (truncated): {doc.page_content[:300]}...")
        else:
            logger.info("No docs or context was found!")
        return inputs

    log_docs_runnable = RunnableLambda(log_docs_step)
