from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging
import uuid  # to generate conversation ID

from .api.chat_handler import ChatHandler
from .config import CORS_ORIGINS

app = FastAPI(
    title="Crustdata API Assistant",
    description="API documentation assistant for Crustdata",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None  # Could be passed or not

class ErrorResponse(BaseModel):
    detail: str

chat_handler = ChatHandler()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/chat")
async def chat(message: ChatMessage):
    """Chat endpoint that handles user messages"""
    try:
        # 1. Generate a UUID if none was provided
        conv_id = message.conversation_id
        if not conv_id:
            conv_id = str(uuid.uuid4())

        # 2. Pass the guaranteed conversation_id to the chat handler
        response = await chat_handler.get_response(
            message=message.message,
            conversation_id=conv_id
        )

        # 3. Ensure we return conversation_id back to the client
        response["conversation_id"] = conv_id

        return response
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request"
        )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logging.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
