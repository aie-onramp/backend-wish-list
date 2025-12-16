# Backend Completion Plan

## Quick Reference: Line-by-Line Changes

### File: `api/index.py`

#### Line 1-6: Update Imports
```python
from fastapi import FastAPI, HTTPException, status  # Add status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field  # Add Field
from openai import OpenAI, APIError, RateLimitError, APIConnectionError  # Add specific errors
import os
from dotenv import load_dotenv
```

#### Line 10: Add FastAPI Metadata
```python
app = FastAPI(
    title="Santa's Chat API",
    description="Chat with St. Nicholas powered by AI",
    version="1.0.0"
)
```

#### Line 22-27: Update ChatRequest and Add ChatResponse
```python
class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str = Field(
        min_length=1,
        max_length=1000,
        description="User message to St. Nicholas"
    )

class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    reply: str = Field(description="AI-generated response")
```

#### Line 29-50: Update Chat Endpoint
```python
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
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OPENAI_API_KEY not configured"
        )
    
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OpenAI API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
```

---

## Implementation Checklist

### Phase 1: Critical Fixes (30 minutes)

- [ ] **Step 1.1:** Update imports (add `status`, `Field`, OpenAI error types)
- [ ] **Step 1.2:** Add FastAPI app metadata (title, description, version)
- [ ] **Step 1.3:** Add `ChatResponse` Pydantic model
- [ ] **Step 1.4:** Add Field validation to `ChatRequest.message`
- [ ] **Step 1.5:** Add return type hint to `chat()` function
- [ ] **Step 1.6:** Add OpenAPI metadata to `@app.post()` decorator
- [ ] **Step 1.7:** Replace dict return with `ChatResponse` model
- [ ] **Step 1.8:** Replace raw status codes with `status.HTTP_*` constants
- [ ] **Step 1.9:** Add specific OpenAI error handling (RateLimitError, APIConnectionError, APIError)

### Phase 2: Verification (10 minutes)

- [ ] **Step 2.1:** Run `python -m py_compile api/index.py` to check syntax
- [ ] **Step 2.2:** Start server: `uvicorn api.index:app --reload`
- [ ] **Step 2.3:** Visit `http://localhost:8000/docs` and verify OpenAPI docs
- [ ] **Step 2.4:** Test health endpoint: `curl http://localhost:8000/`
- [ ] **Step 2.5:** Test chat endpoint with valid message
- [ ] **Step 2.6:** Test chat endpoint with empty message (should return 422)
- [ ] **Step 2.7:** Verify response format matches `ChatResponse` model

### Phase 3: Production Readiness (Optional, 15 minutes)

- [ ] **Step 3.1:** Update CORS for production (document in comments)
- [ ] **Step 3.2:** Add logging (optional, if needed)
- [ ] **Step 3.3:** Review error messages for user-friendliness

---

## Complete Fixed Code

Here's the complete `api/index.py` file with all fixes applied:

```python
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI, APIError, RateLimitError, APIConnectionError
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Santa's Chat API",
    description="Chat with St. Nicholas powered by AI",
    version="1.0.0"
)

# CORS so the frontend can talk to backend
# TODO: Update allow_origins for production deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development only - restrict in production
    allow_methods=["*"],
    allow_headers=["*"]
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str = Field(
        min_length=1,
        max_length=1000,
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
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OPENAI_API_KEY not configured"
        )
    
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OpenAI API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
```

---

## Testing Commands

### Local Testing
```bash
# Start server
uvicorn api.index:app --reload

# Test health check
curl http://localhost:8000/

# Test chat endpoint (requires OPENAI_API_KEY in .env)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, St. Nicholas!"}'

# Test validation (should return 422)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'
```

### Verify OpenAPI Docs
1. Start server: `uvicorn api.index:app --reload`
2. Visit: `http://localhost:8000/docs`
3. Verify:
   - Endpoint shows summary and description
   - Request/Response schemas are documented
   - Error responses (429, 503, 500) are listed

---

## Validation Summary

### ✅ What's Already Good
- FastAPI app structure
- CORS middleware configured
- OpenAI client initialization
- Environment variable loading
- Basic error handling
- Deployment configuration files

### ❌ What Needs Fixing (Critical)
1. Missing `ChatResponse` model
2. Missing type hints on `chat()` function
3. Missing OpenAPI metadata
4. Incomplete error handling (missing specific OpenAI exceptions)
5. Returning dict instead of Pydantic model

### ⚠️ What Should Be Improved (Important)
1. Add Field validation to `ChatRequest.message`
2. Add FastAPI app metadata
3. Use status code constants instead of raw numbers
4. Document production CORS configuration

---

## Estimated Time to Complete

- **Critical fixes:** 30 minutes
- **Testing & verification:** 10 minutes
- **Total:** ~40-45 minutes

---

## Success Criteria

✅ All critical tasks completed  
✅ Code passes type checking  
✅ OpenAPI docs show complete endpoint documentation  
✅ Error handling covers all OpenAI exception types  
✅ Response uses Pydantic model  
✅ All status codes use constants from `fastapi.status`

