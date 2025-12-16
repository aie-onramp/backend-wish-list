# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI backend for "Santa's Magical Wish List" application - part of AI Engineering Onramp Session 3 (Full-Stack LLM Application Development). The backend provides a chat API powered by OpenAI's GPT-4o-mini, featuring a St. Nicholas persona that responds to user messages.

**Key Characteristics:**
- Minimal serverless FastAPI backend designed for Vercel deployment
- Single endpoint architecture (`/api/chat`) for LLM-powered chat
- CORS-enabled for cross-origin frontend communication
- Environment-based configuration (OpenAI API key)

## Architecture

**Technology Stack:**
- **Framework:** FastAPI 0.121.2+
- **Server:** Uvicorn 0.38.0+
- **LLM Integration:** OpenAI API (gpt-4o-mini model)
- **Deployment Target:** Vercel Serverless Functions
- **Python Version:** 3.12+

**Application Structure:**
```
backend-wish-list/
├── api/
│   └── index.py           # Main FastAPI application (single file)
├── pyproject.toml         # Project metadata and dependencies (uv)
├── requirements.txt       # Dependencies for Vercel deployment
├── vercel.json           # Vercel serverless configuration
├── .env.example          # Template for environment variables
└── .env                  # Local secrets (NEVER commit)
```

**Critical Design Pattern:**
- All routes handled by single `api/index.py` file via Vercel routing
- `vercel.json` routes all requests (`/(.*)`) to `/api/index.py`
- CORS middleware configured to allow all origins (`allow_origins=["*"]`)
- No database, no state management - stateless API design
- OpenAI client initialized once at module level for reuse

## Common Development Commands

### Local Development

```bash
# Install dependencies with uv (preferred)
uv sync

# Create .env file from template
cp .env.example .env
# Then edit .env and add your OpenAI API key

# Run development server
uv run uvicorn api.index:app --reload --host 0.0.0.0 --port 8000

# Alternative: Run without uv (if dependencies already installed)
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
```

### Testing Locally

```bash
# Health check
curl http://localhost:8000

# Test chat endpoint
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello Santa!"}'

# Open interactive API documentation
# Visit: http://localhost:8000/docs
```

### Deployment to Vercel

```bash
# Deploy to production
vercel --prod

# CRITICAL: After deployment, set environment variable in Vercel Dashboard
# Project Settings → Environment Variables → Add:
# OPENAI_API_KEY = sk-your-actual-key-here

# Test deployed backend
curl https://your-deployment.vercel.app/
curl https://your-deployment.vercel.app/docs
```

### Dependency Management

```bash
# Add new dependency
uv add package-name

# Update all dependencies
uv sync --upgrade

# Generate requirements.txt from pyproject.toml (for Vercel)
uv pip compile pyproject.toml -o requirements.txt
```

## API Endpoints

### `GET /`
Health check endpoint.

**Response:**
```json
{"status": "ok"}
```

### `POST /api/chat`
Chat with St. Nicholas AI persona.

**Request Body:**
```json
{
  "message": "string"
}
```

**Response:**
```json
{
  "reply": "string"
}
```

**Error Responses:**
- `500` - OpenAI API key not configured
- `500` - Error calling OpenAI API

## Environment Variables

**Required:**
- `OPENAI_API_KEY` - OpenAI API key (starts with `sk-`)

**Configuration:**
- **Local Development:** Set in `.env` file (copy from `.env.example`)
- **Production (Vercel):** Set in Vercel Dashboard → Project Settings → Environment Variables

**Security Rules:**
- `.env` file is gitignored - NEVER commit to repository
- Always use `.env.example` template for sharing configuration structure
- Only commit `.env.example` with placeholder values

## Development Workflow

### Adding New Endpoints

All endpoints must be added to `api/index.py`:

```python
@app.post("/api/new-endpoint")
def new_endpoint(request: RequestModel):
    # Implementation
    return {"result": "data"}
```

### Modifying St. Nicholas Persona

Edit the system prompt in `api/index.py` at api/index.py:39-44:

```python
{"role": "system", "content": """You are St. Nicholas (Mikuláš).
    [Modify persona description here]
"""}
```

### Changing OpenAI Model

Replace `model="gpt-4o-mini"` in `api/index.py` at api/index.py:37 with:
- `gpt-4o` (more capable, higher cost)
- `gpt-4-turbo` (balanced)
- `gpt-3.5-turbo` (faster, lower cost)

## Integration with Frontend

This backend is designed to work with a Next.js frontend (see parent directory `frontend-wish-list/`).

**Frontend Integration Pattern:**
1. Frontend makes POST request to `/api/chat`
2. Backend calls OpenAI API with St. Nicholas persona
3. Response returns to frontend for display

**CORS Configuration:**
- Currently set to `allow_origins=["*"]` for development
- For production, consider restricting to specific frontend URL:
  ```python
  allow_origins=["https://your-frontend.vercel.app"]
  ```

## Common Issues and Solutions

### "OPENAI_API_KEY not configured" Error

**Problem:** Environment variable not set.

**Solutions:**
- **Local:** Verify `.env` file exists and contains `OPENAI_API_KEY=sk-...`
- **Production:** Check Vercel Dashboard → Environment Variables
- **After changes:** Restart uvicorn server (local) or redeploy (Vercel)

### "Port 8000 already in use" Error

**Problem:** Previous uvicorn process still running.

**Solution:**
```bash
# Find and kill process on port 8000
kill -9 $(lsof -ti tcp:8000)
```

### CORS Errors from Frontend

**Problem:** Frontend origin not allowed or CORS middleware misconfigured.

**Solutions:**
- Verify CORS middleware in `api/index.py` includes:
  ```python
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"]
  ```
- Check browser console for exact CORS error message
- Ensure OPTIONS preflight requests are handled (FastAPI does this automatically)

### OpenAI API Errors

**Problem:** Rate limits, invalid API key, or model access issues.

**Solutions:**
- Verify API key is valid and has credits at platform.openai.com
- Check OpenAI usage limits and quotas
- Ensure model name is spelled correctly (`gpt-4o-mini`)
- Review OpenAI API error message in backend logs

## Vercel Deployment Configuration

### vercel.json Explanation

```json
{
  "version": 2,
  "routes": [
    { "src": "/(.*)", "dest": "/api/index.py" }
  ]
}
```

**Purpose:**
- Routes all incoming requests to `/api/index.py`
- Enables FastAPI to handle routing internally
- Required for Vercel serverless function deployment

### Deployment Requirements

1. Both `pyproject.toml` AND `requirements.txt` must be present
   - Vercel uses `requirements.txt` to install dependencies
   - `uv` uses `pyproject.toml` for local development

2. `api/index.py` must define `app` variable as FastAPI instance
   - Vercel looks for `app` in the specified destination file

3. Environment variables must be set in Vercel Dashboard
   - Cannot rely on `.env` file in production

## Testing

### Manual Testing Workflow

1. Start local server: `uv run uvicorn api.index:app --reload --port 8000`
2. Open browser to `http://localhost:8000/docs`
3. Click on `/api/chat` endpoint → "Try it out"
4. Enter test message in request body:
   ```json
   {"message": "Am I naughty or nice?"}
   ```
5. Click "Execute" and verify response

### Testing After Deployment

1. Visit deployed URL: `https://your-backend.vercel.app/docs`
2. Test health endpoint: `https://your-backend.vercel.app/`
3. Test chat endpoint using Swagger UI at `/docs`
4. Check Vercel function logs for errors: Dashboard → Deployments → [deployment] → View Function Logs

## Code Style and Patterns

### Error Handling Pattern

Always use FastAPI's `HTTPException` for errors:

```python
from fastapi import HTTPException

if not condition:
    raise HTTPException(status_code=500, detail="Error message")
```

### Request/Response Models

Use Pydantic `BaseModel` for type validation:

```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
```

### OpenAI Client Pattern

Client is initialized once at module level:

```python
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

Do NOT recreate client on every request - reuse the module-level instance.

## Important Notes

1. **Single File Architecture:** This is intentionally minimal - all code in one file (`api/index.py`)
2. **No Database:** Stateless design - no persistence layer
3. **No Authentication:** Educational project - no auth/authorization implemented
4. **Session 3 Context:** This backend is part of a larger assignment connecting frontend to backend
5. **Parent Project:** See `CHEATSHEET.md` and `README.md` for full session context

## Related Files

- `CHEATSHEET.md` - Session 3 complete reference guide
- `README.md` - Assignment instructions and deployment steps
- `diagrams.md` - Architecture diagrams (if present)
- `.env.example` - Template for environment variables
- `vercel.json` - Serverless function configuration
