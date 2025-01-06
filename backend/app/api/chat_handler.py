from typing import Dict, Optional
import faiss
from langchain.vectorstores import faiss
from langchain_community.docstore import InMemoryDocstore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser

from .. config import  VECTOR_STORE_DIR, MODEL_SETTINGS
from ..agents.crustdata_agent import CrustDataAgent
from ..utils import save_vectorstore, load_vectorstore
from ..utils.logger import logger
from ..utils.text_processor import clean_text, format_api_response


# ... your other imports ...

class ChatHandler:
    def __init__(self):
        logger.info("Initializing ChatHandler")

        # Initialize RAG components
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.vectorstore = self.initialize_vectorstore()
        self.llm = ChatOpenAI(
            model_name=MODEL_SETTINGS["chat_model"],
            temperature=MODEL_SETTINGS["temperature"]
        )

        # Initialize agent
        self.agent = CrustDataAgent()

        # Create retrieval chain
        self.retrieval_chain = self.create_retrieval_chain()
        logger.info("ChatHandler initialized successfully")

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

    def create_retrieval_chain(self):
        """Create the RAG retrieval chain"""
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

        prompt = ChatPromptTemplate.from_messages([
            ("system", """Use the following pieces of API documentation to answer the user's question.
                          Always provide code examples when available in the documentation.
                          If specific information isn't found in the context, say that you don't have that specific information in the documentation.
                          Format API examples using markdown code blocks.

            Context: {context}"""),
            ("user", "{question}")
        ])

        chain = (
                {
                    "context": retriever,
                    "question": RunnablePassthrough()
                }
                | prompt
                | self.llm
                | StrOutputParser()
        )

        return chain

    def create_validation_chain(self):
        """Create chain for API validation and fixing"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an API validation assistant. 
            Analyze the API call and any errors, then suggest specific fixes.
            Include code examples in your response.

            Previous conversation context: {conversation_context}
            API call: {api_call}
            Validation result: {validation_result}"""),
            ("user", "What fixes or improvements would you suggest for this API call?")
        ])

        return prompt | self.llm | StrOutputParser()

    def _plan_actions(self, message: str) -> List[AgentAction]:
        """Determine necessary actions based on message content"""
        actions = []

        # Check for API calls
        if "curl" in message.lower() or "api" in message.lower():
            actions.append(AgentAction.VALIDATE_API)

        # Check for error messages
        if any(err in message.lower() for err in ["error", "failed", "doesn't work", "wrong"]):
            actions.append(AgentAction.FIX_ERROR)

        # Check for region-related queries
        if "region" in message.lower() and "error" in message.lower():
            actions.append(AgentAction.SUGGEST_ALTERNATIVES)

        return actions

    def _extract_api_calls(self, text: str) -> List[str]:
        """Extract API calls from text"""
        curl_commands = re.finditer(r"```(?:bash|shell)?\s*(curl .*?)```", text, re.DOTALL)
        return [match.group(1).strip() for match in curl_commands]

    async def _handle_api_validation(self, api_call: str) -> Dict:
        """Handle API validation and fixes"""
        # Validate API call
        is_valid, error_msg, fixes = self.api_validator.validate_api_call(api_call)

        if not is_valid:
            # Get fixed version if available
            fixed_call = self.error_fixer.fix_api_call(api_call, error_msg, fixes)

            # Get explanation using validation chain
            explanation = await self.validation_chain.ainvoke({
                "api_call": api_call,
                "validation_result": error_msg,
                "conversation_context": self.conversation_state
            })

            return {
                "is_valid": False,
                "error": error_msg,
                "fixed_call": fixed_call,
                "explanation": explanation
            }

        return {"is_valid": True}

    async def get_response(self, message: str, conversation_id: Optional[str] = None) -> Dict:
        """Enhanced message processing with agentic behavior"""
        try:
            logger.info(f"Processing message: {message[:50]}...")

            # Update conversation state
            if conversation_id not in self.conversation_state:
                self.conversation_state[conversation_id] = []
            self.conversation_state[conversation_id].append({"role": "user", "content": message})

            # Clean input
            cleaned_message = clean_text(message)

            # Plan actions
            actions = self._plan_actions(cleaned_message)
            response_parts = []

            # Execute planned actions
            for action in actions:
                if action == AgentAction.VALIDATE_API:
                    api_calls = self._extract_api_calls(cleaned_message)
                    for api_call in api_calls:
                        validation_result = await self._handle_api_validation(api_call)
                        if not validation_result["is_valid"]:
                            response_parts.append(
                                f"I noticed an issue with your API call:\n\n"
                                f"{validation_result['explanation']}\n\n"
                                f"Here's the corrected version:\n```bash\n{validation_result['fixed_call']}\n```"
                            )

                elif action == AgentAction.FIX_ERROR:
                    fixes = self.error_fixer.analyze_error({"message": cleaned_message})
                    if fixes:
                        response_parts.append(
                            f"I can help fix that error. Here are the suggested fixes:\n"
                            f"{self.error_fixer.get_fix_explanation()}"
                        )

                elif action == AgentAction.SUGGEST_ALTERNATIVES:
                    suggestions = self._suggest_alternatives(cleaned_message)
                    if suggestions:
                        response_parts.append(
                            f"Here are some alternative approaches you might find helpful:\n"
                            f"{suggestions}"
                        )

            # Get base response from RAG chain
            rag_response = await self.retrieval_chain.ainvoke(cleaned_message)
            response_parts.insert(0, rag_response)  # Add RAG response at the beginning

            # Combine responses
            final_response = "\n\n".join(response_parts)
            formatted_response = format_api_response(final_response)

            # Update conversation state
            self.conversation_state[conversation_id].append(
                {"role": "assistant", "content": formatted_response}
            )

            logger.info("Successfully generated enhanced response")

            return {
                "response": formatted_response,
                "conversation_id": conversation_id,
                "state": {
                    "actions_taken": [a.value for a in actions],
                    "conversation_length": len(self.conversation_state.get(conversation_id, []))
                }
            }

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "response": "I apologize, but I encountered an error. Please try again.",
                "conversation_id": conversation_id,
                "error": str(e)
            }

    def _suggest_alternatives(self, message: str) -> str:
        """Generate alternative suggestions based on context"""
        if "region" in message.lower():
            return (
                "1. You can use our region normalization endpoint first\n"
                "2. Check the complete list of supported regions at our docs\n"
                "3. Try using the parent region (e.g., 'United States' instead of specific city)"
            )
        return ""


class ErrorFixer:
    """Handles API error analysis and fixes"""

    def __init__(self):
        self._last_fix_explanation = ""

    def analyze_error(self, error_context: Dict) -> List[Dict]:
        """Analyze API errors and suggest fixes"""
        fixes = []
        error_message = error_context.get("message", "")

        if "No mapping found for REGION" in error_message:
            fixes.append({
                "type": "region_normalization",
                "description": "Region format needs normalization",
                "action": "normalize_region"
            })
            self._last_fix_explanation = (
                "The region format needs to match our supported regions exactly. "
                "Try using the full region name (e.g., 'San Francisco, California, United States')"
            )

        return fixes

    def get_fix_explanation(self) -> str:
        """Get explanation of the latest fix applied"""
        return self._last_fix_explanation

    def fix_api_call(self, api_call: str, error_msg: str, fixes: Dict) -> str:
        """Apply fixes to an API call"""
        fixed_call = api_call

        for fix_type, fix_value in fixes.items():
            if fix_type == "suggested_region":
                # Apply region fix
                fixed_call = re.sub(
                    r'"([^"]+)"(?=\s*\]\s*}\s*,\s*"filter_type":\s*"REGION")',
                    f'"{fix_value}"',
                    fixed_call
                )

        return fixed_call