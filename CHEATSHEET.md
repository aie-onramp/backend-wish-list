# Session 3 Cheatsheet: Connecting Frontend UIs to Backend Deployments

## Important Clarification: This Builds on Sessions 1 & 2

**Session 3 is NOT starting from scratch.** You're integrating the skills from previous sessions into a complete full-stack application. Here's the progression:

| Session 1 | Session 2 | Session 3 |
|-----------|-----------|-----------|
| Frontend only (Next.js/React) | Backend only (Python/FastAPI) | **Full-Stack Integration** |
| v0.dev generates UI | YOU write backend code | Connect frontend ↔ backend |
| Deploy to Vercel (static/SSR) | Deploy to Vercel (serverless functions) | **Deploy BOTH separately** |
| No backend needed | No frontend needed | **Frontend calls backend APIs** |

**Key Learning Focus:**
- Environment variable management across services
- CORS configuration for cross-origin requests
- API routes as proxy layer
- Dual deployment strategy (frontend + backend separately on Vercel)
- Full-stack debugging and integration testing

---

## What You're Building

A **Complete Full-Stack LLM Application** called "Santa's Magical Wish List":

**Frontend (Next.js 16 + React 19):**
- Wish management system with NICE/NAUGHTY verdicts
- Live chat interface with St. Nicholas
- Spirit meter tracking (0-100% based on wishes)
- Theme unlocking system (Classic, Snow, Aurora, Gingerbread)
- Christmas-themed UI with snowflakes and parchment design

**Backend (FastAPI + OpenAI GPT-4o-mini):**
- Chat endpoint with St. Nicholas AI persona
- OpenAI API integration for intelligent responses
- Automatic API documentation at `/docs`
- CORS middleware for frontend communication

**Deployment:**
- **Frontend**: Vercel → `https://your-frontend.vercel.app`
- **Backend**: Vercel → `https://your-backend.vercel.app`
- Both services communicate via HTTPS in production

---

## High-Level Workflow (8 Steps, ~25 minutes)

This section provides a bird's-eye view of the complete assignment workflow. Detailed instructions follow in later sections.

**Step 1: Create Separate Repositories** (3 min)
- Create two new GitHub repos: `santa-backend` and `santa-frontend`
- Clone both repositories to your local machine

**Step 2: Set Up Backend** (3 min)
- Copy `app/backend-wish-list/` files to `santa-backend` repo using `cp -r`
- Commit and push to GitHub

**Step 3: Test Backend Locally** (3 min)
- Install dependencies with `uv sync`
- Create `.env` file with `OPENAI_API_KEY`
- Run `uvicorn api.index:app --reload`
- Test at `http://localhost:8000/docs`

**Step 4: Deploy Backend to Vercel** (3 min)
- Run `vercel --prod` from backend repository
- Add `OPENAI_API_KEY` in Vercel dashboard
- Note your backend URL (e.g., `https://santa-backend.vercel.app`)

**Step 5: Set Up Frontend** (3 min)
- Copy `app/frontend-wish-list/` files to `santa-frontend` repo using `cp -r`
- Commit and push to GitHub

**Step 6: Test Frontend Locally** (3 min)
- Install dependencies with `npm install`
- Create `.env.local` with `NEXT_PUBLIC_BACKEND_URL=http://localhost:8000`
- Run `npm run dev`
- Test at `http://localhost:3000`

**Step 7: Deploy Frontend to Vercel** (4 min)
- Run `vercel --prod` from frontend repository
- Add `NEXT_PUBLIC_BACKEND_URL` in Vercel dashboard (use deployed backend URL)
- Wait for deployment to complete

**Step 8: Test End-to-End Application** (3 min)
- Visit your deployed frontend URL
- Submit a wish and verify NICE/NAUGHTY verdict appears
- Chat with Santa and verify AI responses work
- **Success!** You have a fully deployed full-stack LLM application

---

## Prerequisites Checklist

Before starting, verify you have:

```bash
# Python 3.12+ (REQUIRED)
python --version  # Must be 3.12+

# Node.js and npm
node --version
npm --version

# uv package manager (Python)
uv --version  # If missing: curl -LsSf https://astral.sh/uv/install.sh | sh

# Vercel CLI
vercel --version  # If missing: npm install -g vercel

# OpenAI API key
echo $OPENAI_API_KEY  # Should show sk-...
```

**Required Accounts:**
- GitHub account (for code hosting)
- Vercel account (for deployment) - sign up at [vercel.com](https://vercel.com)
- OpenAI API key - get at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

## Two Paths: Quick Start vs From Scratch

### Path A: Use the Provided App (Recommended for Beginners)

The course provides a complete working application in the `app/` directory with both frontend and backend ready to deploy.

```bash
# Navigate to Session 3 directory
cd Session_03_Connecting_Frontend_UIs_to_Backend_Deployments/app

# You'll find:
# - backend-wish-list/   (FastAPI backend)
# - frontend-wish-list/  (Next.js frontend)
```

**Pros:**
- Focus on understanding integration patterns
- Complete, tested code to learn from
- Faster setup for deployment practice

**Cons:**
- Less hands-on coding practice
- May not fully understand every line

### Path B: Build Your Own from Scratch

Follow the File-by-File Setup Guide below to create your own implementation.

**Pros:**
- Maximum learning and understanding
- Build muscle memory for full-stack development
- Customize to your preferences

**Cons:**
- More time-consuming
- More opportunities for errors
- Requires careful attention to detail

---

## IMPORTANT: Repository Structure for Deployment

**Critical Understanding:** The `app/` folder in the course repository contains reference code for **both** services. To deploy them, you must **copy each service to its own separate GitHub repository**.

### Required: Create Two Separate Repositories
https://github.com/aie-onramp/aie02_sess03
**Step 1: Create Two New GitHub Repositories**

```bash
# On GitHub:
# 1. Create: your-username/santa-backend
# 2. Create: your-username/santa-frontend
```

**Step 2: Copy Backend to Its Own Repository**

```bash
# Create new backend repository locally
git clone git@github.com:your-username/santa-backend.git
cd santa-backend

# Copy backend files from course repository
cp -r ./app ../

# Initialize and push
git add .
git commit -m "Initial backend setup"
git push origin main
```

**Step 3: Copy Frontend to Its Own Repository**

```bash
# Create new frontend repository locally
git clone git@github.com:your-username/santa-frontend.git
cd santa-frontend

# Copy frontend files from course repository
cp -r ~/path/to/Session_03.../app/frontend-wish-list/* .

# Initialize and push
git add .
git commit -m "Initial frontend setup"
git push origin main
```

**Final Structure:**

```
your-github-account/
├── santa-backend/          (separate repository)
│   ├── api/
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── vercel.json
│   └── .env (local only, not committed)
│
└── santa-frontend/         (separate repository)
    ├── app/
    ├── package.json
    ├── next.config.ts
    └── .env.local (local only, not committed)
```

### Why Separate Repositories?

- **Independent version control** - Each service has its own git history
- **Separate deployments** - Deploy backend and frontend independently
- **Clear service boundaries** - No confusion about what code belongs where
- **Team collaboration** - Different developers can own different services
- **Production-ready pattern** - This is how real-world microservices are structured
- **Vercel integration** - Each repository connects to its own Vercel project

**Important:** Never try to deploy from the course repository's `app/` folder. Always copy to separate repositories first.

---

## File-by-File Setup Guide

### Backend Files

#### 1. `api/index.py` - FastAPI Application

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS so the frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/api/chat")
def chat(request: ChatRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")

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
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")
```

#### 2. `pyproject.toml` - Python Project Metadata

```toml
[project]
name = "backend-wish-list"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.121.2",
    "uvicorn>=0.38.0",
    "openai>=1.0.0",
    "python-dotenv>=1.0.0",
]
```

#### 3. `requirements.txt` - Vercel Compatibility

```
fastapi>=0.121.2
uvicorn>=0.38.0
openai>=1.0.0
python-dotenv>=1.0.0
```

#### 4. `vercel.json` - Serverless Configuration

```json
{
  "version": 2,
  "routes": [
    { "src": "/(.*)", "dest": "/api/index.py" }
  ]
}
```

#### 5. `.env` - Environment Variables (NEVER COMMIT!)

```
OPENAI_API_KEY=sk-your-actual-key-here
```

#### 6. `.gitignore` - Protect Your Secrets

```
.env
.venv/
__pycache__/
*.pyc
.vercel/
```

### Frontend Files

#### 1. `package.json` - Dependencies

```json
{
  "name": "frontend-wish-list",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint ."
  },
  "dependencies": {
    "next": "16.0.7",
    "react": "19.2.1",
    "react-dom": "19.2.1",
    "lucide-react": "^0.454.0",
    "@radix-ui/react-progress": "1.1.1",
    "tailwindcss": "^4.1.9"
  }
}
```

#### 2. `app/api/santa-chat/route.ts` - Chat Proxy to Backend

```typescript
import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { message } = body

    if (!message) {
      return NextResponse.json({ error: "Message is required" }, { status: 400 })
    }

    // Get backend URL from environment variable, fallback to localhost
    // Remove trailing slash to avoid double slashes
    const backendBaseUrl = (process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000").replace(/\/$/, "")
    const backendUrl = `${backendBaseUrl}/api/chat`

    console.log("[santa-chat] Calling backend:", backendUrl)

    const response = await fetch(backendUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    })

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json({ reply: data.reply })
  } catch (error) {
    console.error("[santa-chat] Error:", error)
    return NextResponse.json(
      { error: "Failed to communicate with Santa" },
      { status: 500 }
    )
  }
}
```

#### 3. `.env.local` - Frontend Environment (Local Development)

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

**Important:** For production deployment, set this in Vercel dashboard to your deployed backend URL.

---

## Command Reference

### Local Development

**Backend (Terminal 1):**
```bash
# Navigate to backend directory
cd app/backend-wish-list

# Install dependencies
uv sync

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key" > .env

# Run backend server
uv run uvicorn api.index:app --reload --port 8000

# Backend now running at http://localhost:8000
# API docs at http://localhost:8000/docs
```

**Frontend (Terminal 2):**
```bash
# Navigate to frontend directory
cd app/frontend-wish-list

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8000" > .env.local

# Run frontend dev server
npm run dev

# Frontend now running at http://localhost:3000
```

### Testing Locally

**Test Backend First:**
```bash
# Health check
curl http://localhost:8000

# Test chat endpoint
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello Santa!"}'

# Or use Swagger UI (easier!)
open http://localhost:8000/docs
```

**Test Frontend:**
```bash
# Open browser to http://localhost:3000
# Test wish submission (should show NICE/NAUGHTY verdict)
# Test Santa chat (should get AI responses)
# Check browser console for API call logs
```

### Deployment

**Deploy Backend First:**
```bash
cd app/backend-wish-list

# Deploy to Vercel
vercel --prod

# CRITICAL: Add environment variable in Vercel Dashboard!
# Go to: Project Settings → Environment Variables
# Add: OPENAI_API_KEY = sk-your-key-here

# Test deployed backend
curl https://your-backend.vercel.app/
curl https://your-backend.vercel.app/docs
```

**Deploy Frontend Second:**
```bash
cd app/frontend-wish-list

# Deploy to Vercel
vercel --prod

# CRITICAL: Add environment variable in Vercel Dashboard!
# Go to: Project Settings → Environment Variables
# Add: NEXT_PUBLIC_BACKEND_URL = https://your-backend.vercel.app

# Test deployed frontend
open https://your-frontend.vercel.app
```

### Useful Commands

```bash
# Kill port if stuck
kill -9 $(lsof -ti tcp:8000)  # Backend
kill -9 $(lsof -ti tcp:3000)  # Frontend

# Rebuild frontend dependencies
cd app/frontend-wish-list
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps

# Update Vercel environment variables
vercel env add OPENAI_API_KEY production
vercel env add NEXT_PUBLIC_BACKEND_URL production

# View Vercel logs
vercel logs [deployment-url]
```

---

## Testing Your Full-Stack Application

### Local Testing Workflow

1. **Start Backend First:**
   ```bash
   cd app/backend-wish-list
   uv run uvicorn api.index:app --reload --port 8000
   ```
   - Verify at http://localhost:8000 (should show `{"status": "ok"}`)
   - Visit http://localhost:8000/docs (should show Swagger UI)
   - Test `/api/chat` endpoint in Swagger UI

2. **Start Frontend Second:**
   ```bash
   cd app/frontend-wish-list
   npm run dev
   ```
   - Verify at http://localhost:3000 (should show Santa's Wish List page)
   - Check browser console for any errors

3. **Test Integration:**
   - Submit a wish (e.g., "I want a new bike")
   - Verify it gets a NICE or NAUGHTY verdict
   - Send a message in Santa chat
   - Verify you get an AI response from St. Nicholas
   - Check browser DevTools Network tab to see API calls

4. **Check Browser Console:**
   - Look for `[santa-chat] Calling backend:` logs
   - Verify backend URL is correct (http://localhost:8000/api/chat)
   - Check for any CORS errors (should be none)

### Production Testing Workflow

1. **Test Backend Independently:**
   ```bash
   # Health check
   curl https://your-backend.vercel.app/

   # API docs
   open https://your-backend.vercel.app/docs

   # Test chat endpoint
   curl -X POST "https://your-backend.vercel.app/api/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "Test message"}'
   ```

2. **Test Frontend:**
   - Visit https://your-frontend.vercel.app
   - Submit wishes and verify verdicts work
   - Test Santa chat and verify AI responses
   - Check browser console for errors

3. **Verify Environment Variables:**
   - Go to Vercel dashboard
   - Check Project Settings → Environment Variables
   - Backend should have: `OPENAI_API_KEY`
   - Frontend should have: `NEXT_PUBLIC_BACKEND_URL`

4. **Check Vercel Logs:**
   - Go to Vercel dashboard → Deployments → [your deployment]
   - Click "View Function Logs"
   - Look for errors or issues

---

## Common Issues & Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| Frontend can't reach backend | `NEXT_PUBLIC_BACKEND_URL` not set | Add to `.env.local` (local) or Vercel dashboard (production) |
| CORS errors in browser | Backend not allowing frontend origin | Verify CORS middleware in `api/index.py` has `allow_origins=["*"]` |
| React version mismatch error | `react` vs `react-dom` versions differ | Ensure both are `19.2.1` in `package.json`, delete `node_modules`, reinstall |
| Backend returns 500 error | `OPENAI_API_KEY` missing or invalid | Add to `.env` (local) or Vercel dashboard (production), verify format starts with `sk-` |
| Port 3000 already in use | Previous dev server running | `kill -9 $(lsof -ti tcp:3000)` |
| Port 8000 already in use | Previous uvicorn running | `kill -9 $(lsof -ti tcp:8000)` |
| npm install fails | Peer dependency conflicts | Use `npm install --legacy-peer-deps` |
| Backend deployment fails | Missing `requirements.txt` | Ensure file exists in backend root with all dependencies |
| Chat returns "Failed to communicate with Santa" | Backend URL has double slashes | Remove trailing slash from `NEXT_PUBLIC_BACKEND_URL` |
| Wish verdicts don't appear | Frontend can't parse backend response | Check browser console for errors, verify backend returns `{"reply": "..."}` |
| OpenAI rate limit error | Too many requests to OpenAI | Wait 60 seconds, check your OpenAI usage limits |
| Vercel deployment succeeds but app doesn't work | Environment variables not set | Add env vars in Vercel dashboard, redeploy |

---

## Assignment Checklist

### Part 1: Required (Minimum to Pass)

**Backend Setup:**
- [ ] Clone repository and navigate to Session 3 directory
- [ ] Set up backend project structure
- [ ] Create `api/index.py` with FastAPI application
- [ ] Create `pyproject.toml`, `requirements.txt`, `vercel.json`
- [ ] Install dependencies with `uv sync`
- [ ] Create `.env` file with `OPENAI_API_KEY`
- [ ] Test backend locally at http://localhost:8000
- [ ] Test `/docs` endpoint (Swagger UI)
- [ ] Test `/api/chat` endpoint with curl or Swagger

**Backend Deployment:**
- [ ] Deploy backend to Vercel with `vercel --prod`
- [ ] Add `OPENAI_API_KEY` to Vercel environment variables
- [ ] Test deployed backend API (health check and `/api/chat`)
- [ ] Verify `/docs` endpoint works on deployed URL

**Frontend Setup:**
- [ ] Set up frontend project structure
- [ ] Install dependencies with `npm install`
- [ ] Create `.env.local` with `NEXT_PUBLIC_BACKEND_URL=http://localhost:8000`
- [ ] Create `app/api/santa-chat/route.ts` (proxy to backend)
- [ ] Test frontend locally at http://localhost:3000
- [ ] Verify frontend can communicate with local backend
- [ ] Test wish submission (should call backend)
- [ ] Test Santa chat (should get AI responses)

**Frontend Deployment:**
- [ ] Deploy frontend to Vercel with `vercel --prod`
- [ ] Add `NEXT_PUBLIC_BACKEND_URL` to Vercel (deployed backend URL)
- [ ] Test deployed frontend application
- [ ] Verify wish evaluation works in production
- [ ] Verify Santa chat works in production
- [ ] Submit both deployment URLs for grading

### Part 2: Advanced (Optional Extra Credit)

**Multi-Persona Chat:**
- [ ] Add Angel persona to backend (emotional, sparkly, believes in redemption)
- [ ] Add Devil persona to backend (sarcastic, chaotic, funny threats)
- [ ] Create persona selector UI in frontend
- [ ] Implement persona switching in API routes
- [ ] Test all three personas work correctly

**Enhanced Features:**
- [ ] Implement CV upload functionality (PDF parsing)
- [ ] Add student questionnaire for personalized responses
- [ ] Implement conversation history (store chat messages)
- [ ] Add error boundary components for graceful error handling
- [ ] Implement loading states with skeletons
- [ ] Add authentication (optional)

---

## Understanding Frontend-Backend Integration

### Key Concepts

#### 1. API Routes as Proxy Layer

Next.js API routes (`app/api/santa-chat/route.ts`) act as **middleware** between the browser and FastAPI backend:

**Why use a proxy?**
- Securely manage environment variables (backend URL)
- Add authentication/authorization logic
- Transform requests/responses
- Implement caching
- Provide debugging logs

**Data Flow:**
```
Browser → Next.js API Route → FastAPI Backend → OpenAI → Response back
```

#### 2. Environment Variable Management

**Critical Differences:**

| Environment | File | Variable | Purpose |
|-------------|------|----------|---------|
| **Local Backend** | `.env` | `OPENAI_API_KEY=sk-...` | OpenAI authentication |
| **Local Frontend** | `.env.local` | `NEXT_PUBLIC_BACKEND_URL=http://localhost:8000` | Points to local backend |
| **Production Backend** | Vercel Dashboard | `OPENAI_API_KEY=sk-...` | OpenAI authentication |
| **Production Frontend** | Vercel Dashboard | `NEXT_PUBLIC_BACKEND_URL=https://...vercel.app` | Points to deployed backend |

**Important Rules:**
- `NEXT_PUBLIC_` prefix required for client-side access in Next.js
- Backend uses `.env` for `OPENAI_API_KEY` (NEVER commit to git!)
- Frontend needs backend URL to make API calls
- Always restart dev servers after changing `.env` files

#### 3. CORS (Cross-Origin Resource Sharing)

**Problem:** By default, browsers block requests from one domain (frontend) to another (backend) for security.

**Solution:** Backend must explicitly allow frontend origin using CORS middleware:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (development)
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"]   # Allow all headers
)
```

**Production Consideration:** For better security, replace `["*"]` with specific frontend URL: `["https://your-frontend.vercel.app"]`

#### 4. Dual Deployment Strategy

**Why deploy separately?**
- **Scalability**: Frontend and backend can scale independently
- **Technology flexibility**: Use best tool for each layer (Next.js vs FastAPI)
- **Separation of concerns**: Frontend handles UI, backend handles business logic
- **Cost efficiency**: Vercel optimizes each service type differently

**Architecture:**
```
User Browser
    ↓
Frontend Vercel Deployment (Next.js)
    ↓ (HTTPS API calls)
Backend Vercel Deployment (FastAPI)
    ↓ (OpenAI API calls)
OpenAI GPT-4o-mini
```

#### 5. Error Handling and Graceful Degradation

Frontend should continue functioning even if backend fails:

```typescript
try {
  const response = await fetch(backendUrl, { /* ... */ })
  // Process response
} catch (error) {
  console.error("Backend error:", error)
  return NextResponse.json(
    { error: "Failed to communicate with Santa" },
    { status: 500 }
  )
}
```

**Best Practices:**
- Show user-friendly error messages
- Log detailed errors to console for debugging
- Provide fallback behavior where possible
- Don't expose sensitive error details to users

---

## Quick Decision Guide

```
Q: Should I use the provided app or build from scratch?
A: Use provided app if you want to focus on understanding integration patterns.
   Build from scratch if you want maximum learning and coding practice.

Q: Do I need to deploy backend before frontend?
A: Yes! Frontend needs the deployed backend URL to communicate in production.
   Set NEXT_PUBLIC_BACKEND_URL in frontend Vercel dashboard to your backend URL.

Q: Can I test frontend without backend running?
A: Frontend will load, but chat and wish features won't work without backend.
   Always run both services for integration testing.

Q: What if my React versions don't match?
A: Edit package.json to ensure "react" and "react-dom" are both "19.2.1".
   Delete node_modules and package-lock.json, then run npm install.

Q: How do I know if my environment variables are set correctly?
A: Local: Check .env and .env.local files exist with correct values.
   Production: Vercel Dashboard → Project Settings → Environment Variables.
   Always restart dev servers after changing .env files.

Q: Does this connect to my Session 1 or Session 2 projects?
A: No! This is a new standalone application that demonstrates full-stack integration.
   However, you CAN apply these patterns to connect your previous projects.

Q: Why are backend and frontend in the same app/ folder if deployed separately?
A: The app/ folder contains REFERENCE CODE for learning. To deploy, you must
   copy each service to its own separate GitHub repository using cp -r.
   NEVER deploy directly from the course repository's app/ folder.

Q: Do I create ONE repository or TWO?
A: TWO separate GitHub repositories - one for backend, one for frontend.
   Copy backend-wish-list/ to your-username/santa-backend repo.
   Copy frontend-wish-list/ to your-username/santa-frontend repo.

Q: Do I create ONE Vercel project or TWO?
A: TWO separate Vercel projects - one connected to your backend repo,
   one connected to your frontend repo. Each has its own URL and env vars.

Q: What if backend returns CORS errors?
A: Verify CORS middleware in api/index.py includes:
   allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]

Q: Why is my chat returning "Failed to communicate with Santa"?
A: Check: (1) Backend is running, (2) NEXT_PUBLIC_BACKEND_URL is correct,
   (3) No trailing slash in URL, (4) Backend has OPENAI_API_KEY set.

Q: Can I use different models instead of gpt-4o-mini?
A: Yes! Edit api/index.py and change model="gpt-4o-mini" to any OpenAI model.
   Options: gpt-4o, gpt-4-turbo, gpt-3.5-turbo (check pricing).

Q: How do I debug integration issues?
A: Use browser DevTools Network tab to see API calls and responses.
   Check backend logs in terminal or Vercel dashboard.
   Add console.log statements in API routes.
```

---

## Pro Tips for Peer Supporters

**Top Debugging Strategies:**
1. **Always verify both services are running** - Check `ps aux | grep uvicorn` and `ps aux | grep next` to confirm processes exist
2. **Check environment variables first** - 80% of integration issues stem from misconfigured env vars; verify with `echo $VAR_NAME` or check Vercel dashboard
3. **Use browser DevTools Network tab** - Shows exact API calls, request/response headers, and error details
4. **Test backend independently first** - Use `/docs` Swagger UI to verify backend works before debugging frontend
5. **Watch for trailing slashes in URLs** - `http://localhost:8000/` causes double slashes when concatenated (`http://localhost:8000//api/chat`)
6. **Verify Vercel deployment logs** - Click deployment → "View Function Logs" to see detailed error messages
7. **Don't skip local testing** - Always test locally with both services running before deploying to production

**Common Student Mistakes:**
- **Trying to deploy from course repository** - Must copy to separate repos first (use `cp -r`)
- **Thinking it's ONE repository** - It's TWO separate GitHub repos (backend + frontend)
- **Forgetting to create separate repos** - Backend and frontend must each have their own repository
- **Not copying .gitignore files** - Make sure to copy hidden files with `cp -r`
- Forgetting to add environment variables in Vercel dashboard
- Using `localhost` URLs in production deployments
- Not restarting dev servers after changing `.env` files
- Mixing up `.env` (backend) vs `.env.local` (frontend)
- Deploying frontend before backend (frontend needs backend URL)
- Not checking browser console for error messages

**Quick Diagnostic Questions:**
1. Are both services running? (`localhost:3000` and `localhost:8000`)
2. Did you restart dev servers after changing `.env` files?
3. Does backend work independently? (test with `/docs`)
4. What does browser console show? (check Network tab)
5. Are environment variables set in Vercel dashboard? (screenshot proof)
6. Does backend URL have trailing slash? (should NOT)

---

## Links & Resources

**Documentation:**
- [FastAPI Documentation](https://fastapi.tiangolo.com) - API framework reference
- [Next.js Documentation](https://nextjs.org/docs) - Frontend framework reference
- [Vercel Deployment Docs](https://vercel.com/docs) - Deployment platform guide
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference) - LLM API documentation
- [Next.js Environment Variables](https://nextjs.org/docs/app/building-your-application/configuring/environment-variables) - Env var configuration
- [FastAPI CORS Middleware](https://fastapi.tiangolo.com/tutorial/cors/) - CORS setup guide

**Session Materials:**
- Session 3 README: Comprehensive setup and deployment guide
- Session 1 CHEATSHEET: Frontend development reference
- Session 2 CHEATSHEET: Backend development reference

**Example Deployments:**
- Sample Frontend: https://frontend-wish-list-eta.vercel.app/
- Sample Backend: https://backend-wish-list.vercel.app/
- Sample Backend API Docs: https://backend-wish-list.vercel.app/docs

**Tools:**
- [Vercel CLI Documentation](https://vercel.com/docs/cli) - Command-line deployment
- [uv Package Manager](https://docs.astral.sh/uv/) - Modern Python package manager
- [Swagger UI](https://swagger.io/tools/swagger-ui/) - Interactive API testing

---

## TL;DR - The 10-Minute Version

**Complete Setup and Deployment:**

```bash
# STEP 1: Test Backend Locally
cd app/backend-wish-list
uv sync
echo "OPENAI_API_KEY=sk-your-key-here" > .env
uv run uvicorn api.index:app --reload --port 8000
# Visit http://localhost:8000/docs - Test /api/chat endpoint

# STEP 2: Deploy Backend
vercel --prod
# Go to Vercel Dashboard → Project Settings → Environment Variables
# Add: OPENAI_API_KEY = sk-your-key-here
# Test: https://your-backend.vercel.app/docs

# STEP 3: Test Frontend Locally
cd ../frontend-wish-list
npm install
echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8000" > .env.local
npm run dev
# Visit http://localhost:3000 - Test chat and wishes

# STEP 4: Deploy Frontend
vercel --prod
# Go to Vercel Dashboard → Project Settings → Environment Variables
# Add: NEXT_PUBLIC_BACKEND_URL = https://your-backend.vercel.app
# Test: https://your-frontend.vercel.app

# STEP 5: Verify Production
# Open deployed frontend URL
# Test wish submission (should show NICE/NAUGHTY)
# Test Santa chat (should get AI responses)
```

**Critical Checkpoints:**
1. Backend `/docs` works locally ✓
2. Backend deployed with `OPENAI_API_KEY` env var ✓
3. Frontend works locally with backend ✓
4. Frontend deployed with `NEXT_PUBLIC_BACKEND_URL` env var ✓
5. Production app fully functional ✓

**You're done!**
