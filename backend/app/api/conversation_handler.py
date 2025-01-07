import openai
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class ConversationHandler:
    """
    This class demonstrates:
      - Storing conversation messages
      - Summarizing older messages when we exceed a threshold
      - Building a final context (summary + recent messages)
    """

    def __init__(self,
                 openai_api_key: str,
                 max_messages_without_summary: int = 5,
                 model_name: str = "gpt-3.5-turbo"):
        """
        :param openai_api_key: Your OpenAI API key.
        :param max_messages_without_summary: Number of full messages to keep before summarizing older ones.
        :param model_name: Which ChatGPT model to use for summarization.
        """
        openai.api_key = openai_api_key
        self.max_messages_without_summary = max_messages_without_summary
        self.model_name = model_name

        # Store conversation data in a dictionary:
        #   conversation_id -> {
        #       "messages": List[Dict] of the most recent messages,
        #       "summary": str summarizing older messages
        #   }
        self.conversations: Dict[str, Dict] = {}

    def add_message(self,
                    conversation_id: str,
                    role: str,
                    content: str) -> None:
        """
        Add a user/assistant/system/agent message to the conversation state.
        If the message count exceeds self.max_messages_without_summary,
        we'll auto-summarize the older messages and clear them out.
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = {
                "messages": [],
                "summary": ""
            }

        conv_data = self.conversations[conversation_id]
        conv_data["messages"].append({"role": role, "content": content})
        logger.debug(f"Added {role} message to conversation {conversation_id}: {content[:60]}...")

        # Check if we need to summarize
        if len(conv_data["messages"]) > self.max_messages_without_summary:
            logger.info(f"Message count exceeded threshold for conversation {conversation_id}. Summarizing...")
            self._summarize_and_trim(conversation_id)

    def add_agent_response(self,
                           conversation_id: str,
                           content: str) -> None:
        """
        Helper method to add the agent's response under the 'agent' role.
        Useful if you want to store the agent's commentary/fixes in the conversation.
        """
        logger.info(f"Adding agent response to conversation {conversation_id}.")
        self.add_message(conversation_id=conversation_id, role="agent", content=content)

    def get_context_for_llm(self,
                            conversation_id: str) -> str:
        """
        Build a single string that combines:
          - The existing summary (if any)
          - The most recent messages in full
        This is what you'd typically feed into your LLM for context.
        """
        if conversation_id not in self.conversations:
            return ""

        conv_data = self.conversations[conversation_id]

        summary_text = conv_data.get("summary", "")
        recent_messages = conv_data.get("messages", [])

        # Convert recent messages to text
        recent_text_blocks = []
        for msg in recent_messages:
            role = msg["role"]
            content = msg["content"]
            recent_text_blocks.append(f"{role.upper()}: {content}")

        recent_text = "\n\n".join(recent_text_blocks)

        # Combine the summary + recent raw messages
        if summary_text.strip():
            combined = f"SUMMARY OF EARLIER CONVERSATION:\n{summary_text}\n\nRECENT MESSAGES:\n{recent_text}"
            logger.debug(f"Context for LLM (with summary) for conversation {conversation_id}:\n{combined[:500]}...")
            return combined
        else:
            logger.debug(f"Context for LLM (no summary) for conversation {conversation_id}:\n{recent_text[:500]}...")
            return f"RECENT MESSAGES:\n{recent_text}"

    def _summarize_and_trim(self, conversation_id: str) -> None:
        """
        Summarize the older messages (except for the last N=2 or 3),
        append the summary to conv_data["summary"],
        and remove those older messages from conv_data["messages"].
        """
        conv_data = self.conversations[conversation_id]
        all_msgs = conv_data["messages"]

        # Decide how many to keep in full (e.g., last 2)
        keep_in_full_count = 2
        to_summarize = all_msgs[:-keep_in_full_count]
        to_keep = all_msgs[-keep_in_full_count:]

        logger.info(f"Summarizing {len(to_summarize)} messages for conversation {conversation_id}. Keeping the last {keep_in_full_count} messages in full.")

        # Summarize the older portion
        summary_chunk = self._summarize_messages(to_summarize)

        # Append this new summary chunk to the existing summary
        existing_summary = conv_data.get("summary", "")
        if existing_summary:
            conv_data["summary"] = f"{existing_summary}\n{summary_chunk}".strip()
        else:
            conv_data["summary"] = summary_chunk

        # Now keep only the last few messages in "messages"
        conv_data["messages"] = to_keep

    def _summarize_messages(self, messages: List[Dict]) -> str:
        """
        Use an OpenAI ChatCompletion call to summarize a list of messages.
        For a "demo" approach, we'll do something straightforward.
        In production, you might want more robust prompt engineering.
        """
        if not messages:
            return ""

        conversation_text = "\n".join([
            f"{m['role'].upper()}: {m['content']}"
            for m in messages
        ])

        prompt_text = (
            "Summarize this conversation:\n\n"
            f"{conversation_text}\n\n"
            "Create a concise summary focusing on key points."
        )

        try:
            logger.debug(f"Sending summarization request for conversation:\n{conversation_text[:500]}...")
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                    {"role": "user", "content": prompt_text}
                ],
                temperature=0.7
            )
            summary = response["choices"][0]["message"]["content"].strip()
            logger.debug(f"Received summary: {summary[:500]}...")
            return summary
        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            return f"(Summary unavailable due to error: {e})"
