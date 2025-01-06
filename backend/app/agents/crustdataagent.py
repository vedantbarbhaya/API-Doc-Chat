from typing import List, Dict
import re
from .base import BaseAgent, AgentAction
from .api_validator import APIValidator
from .error_fixer import ErrorFixer
from ..utils.logger import logger


class CrustDataAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.api_validator = APIValidator()
        self.error_fixer = ErrorFixer()
        self.conversation_state = {}

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

    async def process_message(self, message: str, conversation_id: str = None) -> Dict:
        """Process message and return agent actions/suggestions"""
        try:
            # Update conversation state
            if conversation_id not in self.conversation_state:
                self.conversation_state[conversation_id] = []
            self.conversation_state[conversation_id].append({"role": "user", "content": message})

            # Plan actions
            actions = self._plan_actions(message)
            response_parts = []

            # Execute planned actions
            for action in actions:
                if action == AgentAction.VALIDATE_API:
                    api_calls = self._extract_api_calls(message)
                    for api_call in api_calls:
                        validation_result = await self._handle_api_validation(api_call)
                        if not validation_result["is_valid"]:
                            response_parts.append(
                                f"API Issue:\n{validation_result['explanation']}\n\n"
                                f"Corrected version:\n```bash\n{validation_result['fixed_call']}\n```"
                            )

                elif action == AgentAction.FIX_ERROR:
                    fixes = self.error_fixer.analyze_error({"message": message})
                    if fixes:
                        response_parts.append(self.error_fixer.get_fix_explanation())

                elif action == AgentAction.SUGGEST_ALTERNATIVES:
                    suggestions = self._suggest_alternatives(message)
                    if suggestions:
                        response_parts.append(suggestions)

            return {
                "agent_response": "\n\n".join(response_parts) if response_parts else None,
                "actions_taken": [a.value for a in actions],
                "conversation_length": len(self.conversation_state.get(conversation_id, []))
            }

        except Exception as e:
            logger.error(f"Agent error: {e}")
            return {"error": str(e)}

    def _extract_api_calls(self, text: str) -> List[str]:
        """Extract API calls from text"""
        curl_commands = re.finditer(r"```(?:bash|shell)?\s*(curl .*?)```", text, re.DOTALL)
        return [match.group(1).strip() for match in curl_commands]

    async def _handle_api_validation(self, api_call: str) -> Dict:
        """Handle API validation and fixes"""
        is_valid, error_msg, fixes = self.api_validator.validate_api_call(api_call)

        if not is_valid:
            fixed_call = self.error_fixer.fix_api_call(api_call, error_msg, fixes)
            return {
                "is_valid": False,
                "error": error_msg,
                "fixed_call": fixed_call,
                "explanation": self._get_validation_explanation(error_msg)
            }

        return {"is_valid": True}

    def _suggest_alternatives(self, message: str) -> str:
        """Generate alternative suggestions based on context"""
        if "region" in message.lower():
            return (
                "Alternative approaches:\n"
                "1. Use our region normalization endpoint first\n"
                "2. Check the complete list of supported regions\n"
                "3. Try using the parent region (e.g., 'United States' instead of specific city)"
            )
        return ""

    def _get_validation_explanation(self, error_msg: str) -> str:
        """Get human-friendly explanation of validation errors"""
        if "No mapping found for REGION" in error_msg:
            return (
                "The region format needs to match our supported regions exactly. "
                "Try using the complete region name (e.g., 'San Francisco, California, United States')"
            )
        return error_msg