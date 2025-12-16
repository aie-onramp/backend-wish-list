from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI, APIError, RateLimitError, APIConnectionError
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Santa's Chat API",
    description="Chat with St. Nicholas powered by AI",
    version="1.0.0"
)

# CORS so the frontend can talk to backend
# Configure allowed origins from environment variable
# Format: comma-separated list, e.g., "https://app1.com,https://app2.com"
# Defaults to "*" for development if not set
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = (
    allowed_origins_env.split(",") if allowed_origins_env != "*" else ["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False if allowed_origins == ["*"] else True
)

# Validate OpenAI API key before initializing client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.warning("OPENAI_API_KEY not set - API calls will fail")
client = OpenAI(api_key=api_key)

class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str = Field(
        min_length=1,
        max_length=1000,  # ~250 tokens for gpt-4o-mini, prevents excessive API costs
        description="User message to St. Nicholas"
    )

class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    reply: str = Field(description="AI-generated response")

@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok"}

@app.post(
    "/api/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with St. Nicholas",
    description="Send a message to St. Nicholas and receive an AI-generated response.",
    responses={
        200: {"description": "Successful response"},
        400: {"description": "Invalid request"},
        500: {"description": "Server error"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "Service unavailable"}
    }
)
def chat(request: ChatRequest) -> ChatResponse:
    """Process chat message and return AI response."""
    try:
        user_message = request.message
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """You are St. Nicholas (Mikuláš).
                    Jolly, warm, and wise. You're the one who decides if someone gets a treat or goes to hell.
                    Use "Ho ho ho!" occasionally. 
                    Your vibe: warm, supportive, fair but firm.
                    You encourage good behavior and gently warn about bad behavior.
                    Always end on encouragement."""},
                {"role": "user", "content": user_message}
            ]
        )
        return ChatResponse(reply=response.choices[0].message.content)
    
    except RateLimitError:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    except APIConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to OpenAI API"
        )
    except APIError as e:
        # Log full error for debugging (server-side only)
        logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )
    except Exception as e:
        # Log full error for debugging (server-side only)
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )