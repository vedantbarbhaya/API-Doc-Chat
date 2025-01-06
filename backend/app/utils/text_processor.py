import re
from typing import Dict, List
from .logger import logger


def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters
    text = re.sub(r'[^\w\s\-.,;:?!()]', '', text)
    return text.strip()


def format_api_response(response: str) -> str:
    """Format API response with proper markdown"""
    # Ensure code blocks are properly formatted
    response = re.sub(
        r'```(\w+)?\n(.*?)\n```',
        lambda m: f'```{m.group(1) or ""}\n{m.group(2).strip()}\n```',
        response,
        flags=re.DOTALL
    )

    # Format API endpoints consistently
    response = re.sub(
        r'(GET|POST|PUT|DELETE)\s+(/\S+)',
        r'`\1 \2`',
        response
    )

    return response


def format_error_response(error: Exception) -> Dict:
    """Format error response for API"""
    error_type = type(error).__name__
    error_msg = str(error)

    logger.error(f"{error_type}: {error_msg}")

    return {
        "error": {
            "type": error_type,
            "message": error_msg
        }
    }