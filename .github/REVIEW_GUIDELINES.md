# Claude Code Review Guidelines

> **Purpose**: This document defines the project-specific review standards for automated PR reviews. It prevents circular review patterns by establishing clear architecture context and validation phases.

---

## Architecture Context (FastAPI + Vercel Serverless)

This is a **minimal serverless FastAPI backend** with specific architectural constraints:

- **Single endpoint design**: `POST /api/chat` only - no database, no state management
- **Deployment target**: Vercel Serverless Functions (not traditional server)
- **OpenAI integration**: Direct SDK usage with gpt-4o-mini model
- **Stateless design**: No sessions, no persistence, completely stateless
- **Environment-based config**: Development vs production behavior controlled by env vars

---

## Core Standards (from `.cursor/rules/`)

### Python/FastAPI Standards (global.mdc)

**Required Patterns:**
- ✓ Type hints on ALL functions (parameters and return types)
- ✓ Pydantic v2 for request/response validation
- ✓ HTTPException for error handling (no bare exceptions)
- ✓ `logging` module (never use `print()` statements)
- ✓ Environment variables for secrets (never hardcoded)
- ✓ FastAPI `status` module for HTTP codes (not raw integers)

**Forbidden Patterns:**
- ❌ No hardcoded API keys or secrets in code
- ❌ No `print()` statements (use `logger.info/warning/error`)
- ❌ No missing type hints on functions
- ❌ No bare exception catches (use specific exception types)

---

### API Design Standards (api-design.mdc)

**Required Patterns:**
- ✓ Pydantic `BaseModel` for request/response schemas
- ✓ OpenAPI metadata on endpoints: `summary`, `description`, `responses` dict
- ✓ Field validators with constraints (min/max length, etc.)
- ✓ CORS middleware configured for frontend communication
- ✓ **CRITICAL**: Production CORS must restrict to specific origin (NOT `["*"]`)

**Example OpenAPI Metadata:**
```python
@app.post(
    "/api/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with St. Nicholas",
    description="Send a message and receive AI response.",
    responses={
        200: {"description": "Successful response"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "Service unavailable"}
    }
)
```

**Forbidden Patterns:**
- ❌ No wildcard CORS in production (`allow_origins=["*"]`)
- ❌ No missing Pydantic models for request/response
- ❌ No missing OpenAPI metadata (summary, description)
- ❌ No `allow_credentials=True` with wildcard origins (browser CORS error)

---

### OpenAI Integration Standards (ai-integration.mdc)

**Required Patterns:**
- ✓ **Single client instance** initialized at module level (reuse, don't recreate per request)
- ✓ Direct OpenAI SDK usage (no complex frameworks)
- ✓ Specific error handling: `RateLimitError` → 429, `APIConnectionError` → 503, `APIError` → 500
- ✓ Cost awareness: Use `gpt-4o-mini` model for this project
- ✓ API key from environment variable (never hardcoded)

**Example Error Handling:**
```python
try:
    response = client.chat.completions.create(model="gpt-4o-mini", ...)
except RateLimitError:
    raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, ...)
except APIConnectionError:
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, ...)
except APIError as e:
    logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, ...)
```

**Forbidden Patterns:**
- ❌ No recreating OpenAI client on every request (inefficient)
- ❌ No generic exception handling for OpenAI errors (use specific types)
- ❌ No missing error logging for debugging
- ❌ No hardcoded API keys

---

### Security Checklist (Critical)

**Required Security Patterns:**
- ✓ CORS restricted to specific frontend origin(s) - prevents OpenAI API abuse
- ✓ API docs disabled in production (`ENVIRONMENT=production`) - reduces attack surface
- ✓ Environment variables for `OPENAI_API_KEY` and `ALLOWED_ORIGINS`
- ✓ No `.env` files committed to git
- ✓ Lifespan handler validates config but **warns, doesn't crash** (serverless compatibility)

**Example CORS Configuration:**
```python
# SECURITY: Prevents unauthorized sites from calling backend
allowed_origins_env = os.getenv("ALLOWED_ORIGINS")

if not allowed_origins_env:
    # Local development defaults
    allowed_origins = ["http://localhost:3000", "http://localhost:5173"]
    logger.warning("⚠️  ALLOWED_ORIGINS not set - using local development defaults")
else:
    # Production: comma-separated list from environment
    allowed_origins = allowed_origins_env.split(",")
    logger.info(f"✓ CORS configured for origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,     # Specific origins only
    allow_credentials=False,            # No auth system, no credentials needed
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"]
)
```

**Example API Docs Disabling:**
```python
# Disable API docs in production to reduce attack surface
if os.getenv("ENVIRONMENT") == "production":
    docs_url = None
    redoc_url = None
    openapi_url = None
else:
    docs_url = "/docs"
    redoc_url = "/redoc"
    openapi_url = "/openapi.json"

app = FastAPI(
    title="Santa's Chat API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url
)
```

---

### Deployment Standards (Vercel Serverless)

**Required Patterns:**
- ✓ Both `pyproject.toml` AND `requirements.txt` present
- ✓ `requirements.txt` = **production dependencies only** (Vercel uses this)
- ✓ `pyproject.toml` = all dependencies including test (local dev uses `uv sync`)
- ✓ Lifespan handler compatible with serverless cold starts (warns, doesn't raise exceptions)
- ✓ `vercel.json` routes all requests to `/api/index.py`

**Critical Understanding:**
- **Test dependencies belong in `pyproject.toml` `[project.optional-dependencies]`**
- **Adding test deps to `requirements.txt` increases cold start time unnecessarily**
- **Vercel supports lifespan events** (as of 2024), but raising exceptions breaks cold starts

**Forbidden Patterns:**
- ❌ No test dependencies in `requirements.txt` (pytest, httpx belong in pyproject.toml)
- ❌ No `raise RuntimeError()` in lifespan handler (breaks serverless cold starts)
- ❌ No assuming Vercel doesn't support lifespan events (outdated assumption)

---

## Git Workflow Standards (git-workflow.mdc)

**Conventional Commits Format:**
```
type(scope): description

[optional body]

[optional footer]
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`, `ci`

**Never Commit:**
- ❌ `.env` files with secrets
- ❌ `__pycache__/` directories
- ❌ `.venv/` virtual environments
- ❌ API keys or credentials
- ❌ IDE-specific files (.vscode/, .idea/)

---

## Anti-Circular Review Logic

### Phase Structure (Prevents Circular Patterns)

```
Phase 1: Current State Validation
         ↓ [GATE: "Based on Phase 1..."]
Phase 2: Gap Analysis (ONLY NEW ISSUES)
         ↓ [GATE: "For gaps in Phase 2..."]
Phase 3: Recommendations (FORWARD-LOOKING)
         ↓ [GATE: "Filter by priority..."]
Phase 4: Prioritization (ACTIONABLE ITEMS)
```

**Key Prevention Mechanisms:**
1. Each phase depends on **previous phase output** (DAG structure, no backward loops)
2. Explicit "DO NOT re-validate Phase N-1" instructions
3. "Based on [previous output]" dependency chains establish forward progression
4. Clear entry/exit criteria for each phase

### DO NOT Re-Review (Anti-Pattern Prevention)

**DO NOT flag these as issues if they already exist correctly:**
- ❌ DO NOT suggest adding lifespan handler if it already exists
- ❌ DO NOT flag module-level OpenAI client initialization as a problem (it's correct)
- ❌ DO NOT recommend adding test deps to requirements.txt (they belong in pyproject.toml)
- ❌ DO NOT suggest removing lifespan handler for serverless (Vercel supports it)
- ❌ DO NOT re-validate items that passed Phase 1 validation

**Example Circular Pattern to AVOID:**
```
First review: "Add lifespan for startup validation"
Developer adds lifespan with RuntimeError
Second review: "Lifespan breaks Vercel - remove it"
Developer removes lifespan
Third review: "No startup validation - add lifespan" ← CIRCULAR!
```

**Correct Pattern:**
```
Phase 1: Validates lifespan EXISTS but raises exception
Phase 2: Identifies gap - "raises RuntimeError breaks cold starts"
Phase 3: Recommends - "Change to logger.warning() instead"
Phase 4: Priority - HIGH (affects deployment)
[No re-validation of lifespan existence in future reviews]
```

---

## Review Priority Levels

**CRITICAL (Security/Deployment Blockers):**
- Wildcard CORS allowing API abuse
- Hardcoded API keys or secrets
- Missing environment variable validation
- Public API docs in production
- Deployment configuration errors

**HIGH (Reliability/Code Quality):**
- Missing error handling for OpenAI errors
- Lifespan handler raising exceptions (breaks serverless)
- Missing type hints on functions
- Missing Pydantic models
- Incorrect HTTP status codes

**MEDIUM (Best Practices):**
- Missing OpenAPI metadata
- Incomplete Field validators
- Missing logging statements
- Inconsistent naming conventions

**LOW (Style/Documentation):**
- Missing docstrings (only if significant)
- Documentation updates
- Comment improvements

---

## Common False Positives (DO NOT Flag)

These patterns are **CORRECT** for this project:

✅ **Module-level OpenAI client initialization** - Correct pattern for reuse
✅ **requirements.txt without test deps** - Correct for Vercel deployment
✅ **Lifespan handler exists** - Correct for startup validation (as long as it warns, doesn't crash)
✅ **Single file architecture** - Correct for minimal serverless design
✅ **No database imports** - Correct for stateless design

---

## Testing Checklist

When reviewing PRs, verify:

1. **Syntax Check**: Code compiles without errors
2. **Server Starts**: Application starts successfully (local or Vercel)
3. **Health Endpoint**: `GET /` returns `{"status": "ok"}`
4. **API Endpoint**: `POST /api/chat` responds correctly
5. **Field Validation**: Empty/invalid messages return 422
6. **OpenAPI Docs**: `/docs` accessible in development, 404 in production
7. **Error Handling**: Rate limits, connection errors handled gracefully
8. **CORS**: Frontend can call backend without browser errors

---

## References

**Official Documentation:**
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)
- [Conditional OpenAPI Docs](https://fastapi.tiangolo.com/how-to/conditional-openapi/)
- [Vercel FastAPI Deployment](https://vercel.com/docs/frameworks/backend/fastapi)
- [Vercel Lifespan Support](https://vercel.com/changelog/fastapi-lifespan-events-are-now-supported-on-vercel)

**Project Documentation:**
- `.cursor/rules/global.mdc` - Python/FastAPI conventions
- `.cursor/rules/api-design.mdc` - API patterns and CORS
- `.cursor/rules/ai-integration.mdc` - OpenAI integration patterns
- `CLAUDE.md` - Architecture and security documentation

---

**Last Updated**: 2025-12-16
**Maintainer**: Project team
**Purpose**: Prevent circular review patterns and establish project-aware automated reviews
