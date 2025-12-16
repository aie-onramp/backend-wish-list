# AIE OnRamp Session 3 - Visual Diagrams

This document provides visual diagrams to help understand the full-stack integration patterns, deployment architecture, and debugging workflows covered in Session 3: Connecting Frontend UIs to Backend Deployments.

---

## 1. Session 3 Context: Building on Sessions 1 & 2

This diagram shows how Session 3 integrates the skills learned in previous sessions into a complete full-stack application.

```mermaid
graph TB
    subgraph "Session 1: Frontend Only"
        S1_TECH[v0.dev + Next.js]
        S1_FOCUS[UI Generation<br/>React Components<br/>Styling]
        S1_DEPLOY[Vercel Static/SSR<br/>Frontend Only]
    end

    subgraph "Session 2: Backend Only"
        S2_TECH[FastAPI + OpenAI]
        S2_FOCUS[API Endpoints<br/>LLM Integration<br/>Business Logic]
        S2_DEPLOY[Vercel Serverless<br/>Backend Only]
    end

    subgraph "Session 3: Full-Stack Integration"
        S3_TECH[Next.js + FastAPI]
        S3_FOCUS[Frontend ↔ Backend<br/>Dual Deployment<br/>Environment Variables<br/>CORS & API Proxy]
        S3_DEPLOY[Vercel Dual Deploy<br/>Frontend + Backend]
    end

    S1_TECH --> S3_TECH
    S2_TECH --> S3_TECH
    S1_FOCUS --> S3_FOCUS
    S2_FOCUS --> S3_FOCUS
    S1_DEPLOY --> S3_DEPLOY
    S2_DEPLOY --> S3_DEPLOY

    style S1_TECH fill:#0ea5e9,color:#fff
    style S2_TECH fill:#009688,color:#fff
    style S3_TECH fill:#7c3aed,color:#fff
    style S3_DEPLOY fill:#22c55e,color:#fff
```

---

## 2. Repository Setup Workflow: From Course Code to Deployment

This diagram shows the required workflow for copying reference code into separate repositories for deployment.

```mermaid
graph TB
    subgraph "Course Repository (Reference Code)"
        COURSE[AIE02 Course Repo<br/>Session_03.../app/]

        subgraph "Reference Backend"
            REF_BE[backend-wish-list/]
            REF_BE_FILES[api/index.py<br/>pyproject.toml<br/>vercel.json]
        end

        subgraph "Reference Frontend"
            REF_FE[frontend-wish-list/]
            REF_FE_FILES[app/page.tsx<br/>package.json<br/>next.config.ts]
        end

        COURSE --> REF_BE
        COURSE --> REF_FE
        REF_BE --> REF_BE_FILES
        REF_FE --> REF_FE_FILES
    end

    subgraph "Your GitHub Repositories"
        subgraph "Backend Repository"
            BE_REPO[your-username/santa-backend]
            BE_COPY[cp -r backend-wish-list/* .]
            BE_COMMIT[git add .<br/>git commit<br/>git push]
        end

        subgraph "Frontend Repository"
            FE_REPO[your-username/santa-frontend]
            FE_COPY[cp -r frontend-wish-list/* .]
            FE_COMMIT[git add .<br/>git commit<br/>git push]
        end
    end

    subgraph "Vercel Deployments"
        subgraph "Backend Vercel"
            BE_VERCEL[Vercel Project 1]
            BE_URL[https://santa-backend.vercel.app]
            BE_ENV[Env: OPENAI_API_KEY]
        end

        subgraph "Frontend Vercel"
            FE_VERCEL[Vercel Project 2]
            FE_URL[https://santa-frontend.vercel.app]
            FE_ENV[Env: NEXT_PUBLIC_BACKEND_URL]
        end
    end

    REF_BE -->|Copy files| BE_COPY
    REF_FE -->|Copy files| FE_COPY

    BE_COPY --> BE_REPO
    FE_COPY --> FE_REPO

    BE_REPO --> BE_COMMIT
    FE_REPO --> FE_COMMIT

    BE_COMMIT -->|Connect & Deploy| BE_VERCEL
    FE_COMMIT -->|Connect & Deploy| FE_VERCEL

    BE_VERCEL --> BE_URL
    BE_VERCEL --> BE_ENV
    FE_VERCEL --> FE_URL
    FE_VERCEL --> FE_ENV

    FE_URL -.->|HTTPS API calls| BE_URL

    style COURSE fill:#e0e7ff,color:#000
    style REF_BE fill:#009688,color:#fff
    style REF_FE fill:#0ea5e9,color:#fff
    style BE_REPO fill:#22c55e,color:#fff
    style FE_REPO fill:#22c55e,color:#fff
    style BE_VERCEL fill:#000,color:#fff
    style FE_VERCEL fill:#000,color:#fff
    style BE_COPY fill:#f59e0b,color:#000
    style FE_COPY fill:#f59e0b,color:#000
```

**Key Takeaway:** The course repository `app/` folder contains **reference code**. You must **copy** each service to its own separate GitHub repository using `cp -r`. NEVER deploy directly from the course repository. Each service needs its own repository connected to its own Vercel project.

---

## 3. Full-Stack Architecture Overview

This diagram shows the complete technology stack and how all components connect in the Santa Wish List application.

```mermaid
graph TB
    subgraph "Development Environment"
        DEV[Developer]
        CURSOR[Cursor IDE]
        TERM1[Terminal 1<br/>Backend: port 8000]
        TERM2[Terminal 2<br/>Frontend: port 3000]
    end

    subgraph "Frontend Stack (Next.js 16)"
        NEXTJS[Next.js Framework]
        REACT[React 19.2.1]
        TAILWIND[Tailwind CSS 4.1.9]
        RADIX[Radix UI Primitives]

        subgraph "API Routes (Proxy Layer)"
            SANTA_API["api/santa-chat"]
            SINGLE_API["api/chat/single"]
        end

        subgraph "Frontend Pages"
            PAGE[app/page.tsx<br/>Wish List UI]
        end
    end

    subgraph "Backend Stack (FastAPI)"
        FASTAPI[FastAPI Framework]
        PYDANTIC[Pydantic Validation]
        UVICORN[Uvicorn Server]
        OPENAI_SDK[OpenAI SDK]

        subgraph "Backend Endpoints"
            ROOT_EP[GET /<br/>Health Check]
            CHAT_EP[POST /api/chat<br/>St. Nicholas AI]
        end
    end

    subgraph "External Services"
        OPENAI[OpenAI API<br/>GPT-4o-mini]
    end

    subgraph "Deployment (Vercel)"
        VERCEL_FE[Frontend Deployment<br/>Serverless Next.js]
        VERCEL_BE[Backend Deployment<br/>Python Functions]
        ENV_FE[NEXT_PUBLIC_BACKEND_URL]
        ENV_BE[OPENAI_API_KEY]
    end

    DEV --> CURSOR
    CURSOR --> TERM1
    CURSOR --> TERM2
    TERM1 --> UVICORN
    TERM2 --> NEXTJS

    NEXTJS --> REACT
    NEXTJS --> TAILWIND
    NEXTJS --> RADIX
    NEXTJS --> PAGE
    NEXTJS --> SANTA_API
    NEXTJS --> SINGLE_API

    UVICORN --> FASTAPI
    FASTAPI --> PYDANTIC
    FASTAPI --> ROOT_EP
    FASTAPI --> CHAT_EP
    FASTAPI --> OPENAI_SDK

    SANTA_API --> CHAT_EP
    SINGLE_API --> CHAT_EP
    OPENAI_SDK --> OPENAI

    NEXTJS --> VERCEL_FE
    ENV_FE --> VERCEL_FE
    FASTAPI --> VERCEL_BE
    ENV_BE --> VERCEL_BE

    VERCEL_FE -.->|HTTPS API calls| VERCEL_BE

    style NEXTJS fill:#0ea5e9,color:#fff
    style FASTAPI fill:#009688,color:#fff
    style OPENAI fill:#7c3aed,color:#fff
    style VERCEL_FE fill:#000,color:#fff
    style VERCEL_BE fill:#000,color:#fff
    style SANTA_API fill:#f59e0b,color:#fff
    style CHAT_EP fill:#22c55e,color:#fff
```

---

## 4. Complete Assignment Workflow (10 Steps)

This flowchart shows the step-by-step process from repository setup through complete deployment.

```mermaid
flowchart TD
    START([Start Assignment]) --> STEP1

    subgraph STEP1_BOX["Step 1: Create Separate Repositories"]
        STEP1[Create GitHub Repos]
        STEP1 --> STEP1A[Create: santa-backend repo]
        STEP1A --> STEP1B[Create: santa-frontend repo]
        STEP1B --> STEP1C[Clone both repos locally]
    end

    subgraph STEP2_BOX["Step 2: Copy Backend Code"]
        STEP2[Copy Backend to Repo]
        STEP2 --> STEP2A[cp -r app/backend-wish-list/* santa-backend/]
        STEP2A --> STEP2B[cd santa-backend]
        STEP2B --> STEP2C[git add . && commit && push]
    end

    STEP1C --> STEP2

    subgraph STEP3_BOX["Step 3: Backend Local Testing"]
        STEP3[Test Backend Locally]
        STEP3 --> STEP3A[uv sync]
        STEP3A --> STEP3B[Create .env with OPENAI_API_KEY]
        STEP3B --> STEP3C[uvicorn api.index:app --reload]
        STEP3C --> STEP3D[Test at localhost:8000/docs]
    end

    STEP2C --> STEP3

    subgraph STEP4_BOX["Step 4: Backend Deployment"]
        STEP4[Deploy Backend to Vercel]
        STEP4 --> STEP4A[vercel --prod]
        STEP4A --> STEP4B[Add OPENAI_API_KEY in Vercel]
        STEP4B --> STEP4C[Test deployed backend]
        STEP4C --> STEP4D[Note backend URL]
    end

    STEP3D --> STEP4

    subgraph STEP5_BOX["Step 5: Copy Frontend Code"]
        STEP5[Copy Frontend to Repo]
        STEP5 --> STEP5A[cp -r app/frontend-wish-list/* santa-frontend/]
        STEP5A --> STEP5B[cd santa-frontend]
        STEP5B --> STEP5C[git add . && commit && push]
    end

    STEP4D --> STEP5

    subgraph STEP6_BOX["Step 6: Frontend Local Testing"]
        STEP6[Test Frontend Locally]
        STEP6 --> STEP6A[npm install]
        STEP6A --> STEP6B[Create .env.local]
        STEP6B --> STEP6C[npm run dev]
        STEP6C --> STEP6D[Test at localhost:3000]
        STEP6D --> STEP6E[Check browser console]
    end

    STEP5C --> STEP6

    subgraph STEP7_BOX["Step 7: Frontend Deployment"]
        STEP7[Deploy Frontend to Vercel]
        STEP7 --> STEP7A[vercel --prod]
        STEP7A --> STEP7B[Add NEXT_PUBLIC_BACKEND_URL<br/>to Vercel]
        STEP7B --> STEP7C[Wait for deployment]
    end

    STEP6E --> STEP7

    subgraph STEP8_BOX["Step 8: Integration Verification"]
        STEP8[Connect Frontend to Backend]
        STEP8 --> STEP8A[Open deployed frontend URL]
        STEP8A --> STEP8B[Verify backend URL is correct]
        STEP8B --> STEP8C[Check Network tab in DevTools]
    end

    STEP7C --> STEP8

    subgraph STEP9_BOX["Step 9: End-to-End Testing"]
        STEP9[Test Full-Stack App]
        STEP9 --> STEP9A[Submit wishes]
        STEP9A --> STEP9B[Verify NICE/NAUGHTY verdicts]
        STEP9B --> STEP9C[Chat with Santa]
        STEP9C --> STEP9D[Verify AI responses]
        STEP9D --> STEP9E[App is LIVE!]
    end

    STEP8C --> STEP9
    STEP9E --> DONE([Assignment Complete!])

    style START fill:#0ea5e9,color:#fff
    style DONE fill:#22c55e,color:#fff
    style STEP9E fill:#10b981,color:#fff
    style STEP1_BOX fill:#dbeafe
    style STEP2_BOX fill:#dcfce7
    style STEP3_BOX fill:#fef3c7
    style STEP4_BOX fill:#e0e7ff
    style STEP5_BOX fill:#dbeafe
    style STEP6_BOX fill:#fef3c7
    style STEP7_BOX fill:#f3e8ff
    style STEP8_BOX fill:#dcfce7
    style STEP9_BOX fill:#d1fae5
```

---

## 5. Wish Evaluation Flow (Sequence Diagram)

This sequence shows how a wish submission flows through the entire system.

```mermaid
sequenceDiagram
    participant User as User Browser
    participant UI as Frontend UI<br/>(page.tsx)
    participant API as API Route<br/>(/api/chat/single)
    participant Backend as FastAPI Backend<br/>(/api/chat)
    participant OpenAI as OpenAI GPT-4o-mini

    User->>UI: Submit wish: "I want a new bike"
    UI->>UI: Update UI state<br/>(show loading)

    UI->>API: POST /api/chat/single<br/>{message: "I want a new bike"}

    Note over API: Get NEXT_PUBLIC_BACKEND_URL<br/>from environment

    API->>Backend: POST /api/chat<br/>{message: "I want a new bike"}

    Backend->>Backend: Validate ChatRequest<br/>(Pydantic)

    Backend->>OpenAI: chat.completions.create()<br/>model: gpt-4o-mini<br/>system: St. Nicholas persona<br/>user: wish message

    Note over OpenAI: LLM processes wish<br/>with St. Nicholas personality

    OpenAI-->>Backend: {choices: [{message: {content: "Ho ho ho!..."}}]}

    Backend-->>API: {reply: "Ho ho ho! A new bike..."}

    API-->>UI: {reply: "Ho ho ho! A new bike..."}

    UI->>UI: Parse response for<br/>NICE/NAUGHTY keywords
    UI->>UI: Add verdict badge<br/>Update wish list

    UI-->>User: Display wish with verdict
```

---

## 6. Santa Chat Flow (Sequence Diagram)

This sequence shows the complete chat message flow from user input to AI response.

```mermaid
sequenceDiagram
    participant User as User Browser
    participant Chat as Chat Interface<br/>(page.tsx)
    participant Proxy as API Route<br/>(/api/santa-chat)
    participant Backend as FastAPI Backend<br/>(/api/chat)
    participant OpenAI as OpenAI API

    User->>Chat: Send message:<br/>"I've been good this year!"

    Chat->>Chat: Add user message to UI<br/>Show loading state with dots

    Chat->>Proxy: POST /api/santa-chat<br/>{message: "I've been good..."}

    Note over Proxy: Load NEXT_PUBLIC_BACKEND_URL<br/>Remove trailing slash
    Proxy->>Proxy: console.log backend URL<br/>(debugging)

    Proxy->>Backend: POST /api/chat<br/>{message: "I've been good..."}

    Backend->>Backend: Check OPENAI_API_KEY exists

    Backend->>OpenAI: chat.completions.create()<br/>model: gpt-4o-mini<br/>system: St. Nicholas prompt

    Note over OpenAI: Generate warm, wise<br/>St. Nicholas response

    OpenAI-->>Backend: AI response with<br/>"Ho ho ho!" and encouragement

    Backend-->>Proxy: {reply: "Ho ho ho! ..."}

    Proxy->>Proxy: console.log response<br/>(debugging)

    Proxy-->>Chat: {reply: "Ho ho ho! ..."}

    Chat->>Chat: Remove loading state<br/>Add Santa message to UI<br/>Scroll to bottom

    Chat-->>User: Display Santa's response
```

---

## 7. Frontend-Backend Communication Patterns

This diagram illustrates the API proxy pattern and how environment variables enable communication.

```mermaid
graph LR
    subgraph "Browser"
        USER_ACTION[User Action<br/>Submit wish / Send chat]
    end

    subgraph "Next.js Frontend (Vercel)"
        UI_COMPONENT[UI Component<br/>page.tsx]

        subgraph "API Routes (Proxy)"
            PROXY_ROUTE[API Route Handler<br/>/api/santa-chat/route.ts]
            ENV_VAR[process.env<br/>NEXT_PUBLIC_BACKEND_URL]
        end

        CORS_SAFE[CORS-safe<br/>Same-origin request]
    end

    subgraph "FastAPI Backend (Vercel)"
        CORS_MIDDLEWARE["CORS Middleware<br/>allow_origins=['*']"]
        ENDPOINT[POST /api/chat<br/>ChatRequest model]
        OPENAI_CLIENT[OpenAI Client]
    end

    subgraph "External API"
        OPENAI_API[OpenAI API<br/>GPT-4o-mini]
    end

    USER_ACTION --> UI_COMPONENT
    UI_COMPONENT -->|fetch /api/santa-chat| PROXY_ROUTE
    PROXY_ROUTE --> ENV_VAR
    ENV_VAR --> CORS_SAFE

    CORS_SAFE -->|HTTP POST<br/>Cross-origin request| CORS_MIDDLEWARE
    CORS_MIDDLEWARE --> ENDPOINT
    ENDPOINT --> OPENAI_CLIENT
    OPENAI_CLIENT --> OPENAI_API

    OPENAI_API -.->|Response| OPENAI_CLIENT
    OPENAI_CLIENT -.->|"{reply: '...'}"| ENDPOINT
    ENDPOINT -.->|JSON response| CORS_MIDDLEWARE
    CORS_MIDDLEWARE -.->|CORS headers added| PROXY_ROUTE
    PROXY_ROUTE -.->|"{reply: '...'}"| UI_COMPONENT

    style PROXY_ROUTE fill:#f59e0b,color:#fff
    style CORS_MIDDLEWARE fill:#22c55e,color:#fff
    style ENDPOINT fill:#009688,color:#fff
    style OPENAI_API fill:#7c3aed,color:#fff
    style ENV_VAR fill:#ef4444,color:#fff
```

---

## 8. Project File Structure

This diagram shows the complete file organization for both frontend and backend services.

```mermaid
graph TD
    ROOT[Session_03/app/]

    subgraph "Backend Structure"
        BE_DIR[backend-wish-list/]
        BE_API[api/]
        BE_INDEX[index.py]
        BE_ENV[.env]
        BE_PY[pyproject.toml]
        BE_REQ[requirements.txt]
        BE_VERCEL[vercel.json]
        BE_GI[.gitignore]
    end

    subgraph "Frontend Structure"
        FE_DIR[frontend-wish-list/]

        subgraph "App Directory"
            FE_APP[app/]
            FE_PAGE[page.tsx]
            FE_LAYOUT[layout.tsx]
            FE_GLOBALS[globals.css]

            subgraph "API Routes"
                FE_API[api/]
                FE_SANTA[santa-chat/route.ts]
                FE_SINGLE[chat/single/route.ts]
            end
        end

        subgraph "Components"
            FE_COMP[components/]
            FE_UI[ui/]
            FE_BUTTON[button.tsx]
            FE_INPUT[input.tsx]
            FE_PROGRESS[progress.tsx]
        end

        subgraph "Public Assets"
            FE_PUB[public/]
            FE_IMG[images/]
            FE_SANTA_IMG[cool-santa.png]
        end

        subgraph "Config Files"
            FE_PKG[package.json]
            FE_NEXT[next.config.ts]
            FE_TS[tsconfig.json]
            FE_ENV_LOCAL[.env.local]
        end
    end

    ROOT --> BE_DIR
    ROOT --> FE_DIR

    BE_DIR --> BE_API
    BE_API --> BE_INDEX
    BE_DIR --> BE_ENV
    BE_DIR --> BE_PY
    BE_DIR --> BE_REQ
    BE_DIR --> BE_VERCEL
    BE_DIR --> BE_GI

    FE_DIR --> FE_APP
    FE_APP --> FE_PAGE
    FE_APP --> FE_LAYOUT
    FE_APP --> FE_GLOBALS
    FE_APP --> FE_API
    FE_API --> FE_SANTA
    FE_API --> FE_SINGLE

    FE_DIR --> FE_COMP
    FE_COMP --> FE_UI
    FE_UI --> FE_BUTTON
    FE_UI --> FE_INPUT
    FE_UI --> FE_PROGRESS

    FE_DIR --> FE_PUB
    FE_PUB --> FE_IMG
    FE_IMG --> FE_SANTA_IMG

    FE_DIR --> FE_PKG
    FE_DIR --> FE_NEXT
    FE_DIR --> FE_TS
    FE_DIR --> FE_ENV_LOCAL

    style BE_INDEX fill:#009688,color:#fff
    style FE_PAGE fill:#0ea5e9,color:#fff
    style BE_ENV fill:#ef4444,color:#fff
    style FE_ENV_LOCAL fill:#ef4444,color:#fff
    style FE_SANTA fill:#f59e0b,color:#fff
    style FE_SINGLE fill:#f59e0b,color:#fff
```

---

## 9. Dual Deployment Architecture (Vercel)

This sequence diagram shows how code gets deployed to Vercel for both frontend and backend.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Git as Git/GitHub
    participant Vercel as Vercel Platform
    participant FE_Lambda as Frontend<br/>Serverless (Next.js)
    participant BE_Lambda as Backend<br/>Serverless (Python)
    participant User as End User

    Note over Dev,Vercel: Backend Deployment Flow

    Dev->>Dev: Write FastAPI code<br/>Test locally (uvicorn)
    Dev->>Git: git push backend code
    Dev->>Vercel: vercel --prod (backend)

    Vercel->>Vercel: Read vercel.json<br/>Detect Python runtime
    Vercel->>Vercel: Install requirements.txt
    Vercel->>Vercel: Build Python function

    alt Build Success
        Vercel->>BE_Lambda: Deploy to serverless
        Vercel-->>Dev: Backend URL<br/>https://backend.vercel.app
    else Build Failure
        Vercel-->>Dev: Error logs
    end

    Dev->>Vercel: Add OPENAI_API_KEY<br/>environment variable

    Note over Dev,Vercel: Frontend Deployment Flow

    Dev->>Dev: Write Next.js code<br/>Test locally (npm run dev)
    Dev->>Git: git push frontend code
    Dev->>Vercel: vercel --prod (frontend)

    Vercel->>Vercel: Detect Next.js app
    Vercel->>Vercel: npm install
    Vercel->>Vercel: next build

    alt Build Success
        Vercel->>FE_Lambda: Deploy to serverless
        Vercel-->>Dev: Frontend URL<br/>https://frontend.vercel.app
    else Build Failure
        Vercel-->>Dev: Error logs
    end

    Dev->>Vercel: Add NEXT_PUBLIC_BACKEND_URL<br/>environment variable

    Note over User,BE_Lambda: Production Request Flow

    User->>FE_Lambda: Visit frontend URL
    FE_Lambda->>BE_Lambda: API call with backend URL
    BE_Lambda-->>FE_Lambda: Response
    FE_Lambda-->>User: Rendered page
```

---

## 10. Local Development Workflow

This flowchart shows how to run both services simultaneously during development.

```mermaid
flowchart LR
    subgraph "Terminal 1: Backend"
        T1_DIR[cd app/backend-wish-list]
        T1_SYNC[uv sync]
        T1_ENV[Create .env with<br/>OPENAI_API_KEY]
        T1_RUN[uv run uvicorn<br/>api.index:app --reload]
        T1_STATUS[Backend running on<br/>127.0.0.1:8000]
    end

    subgraph "Terminal 2: Frontend"
        T2_DIR[cd app/frontend-wish-list]
        T2_INSTALL[npm install]
        T2_ENV[Create .env.local with<br/>NEXT_PUBLIC_BACKEND_URL]
        T2_RUN[npm run dev]
        T2_STATUS[Frontend running on<br/>localhost:3000]
    end

    subgraph "Browser Testing"
        BE_DOCS[Open localhost:8000/docs<br/>Test /api/chat endpoint]
        FE_APP[Open localhost:3000<br/>Test wishes and chat]
        DEVTOOLS[Check Network tab<br/>Verify API calls]
    end

    T1_DIR --> T1_SYNC
    T1_SYNC --> T1_ENV
    T1_ENV --> T1_RUN
    T1_RUN --> T1_STATUS

    T2_DIR --> T2_INSTALL
    T2_INSTALL --> T2_ENV
    T2_ENV --> T2_RUN
    T2_RUN --> T2_STATUS

    T1_STATUS --> BE_DOCS
    T2_STATUS --> FE_APP
    FE_APP --> DEVTOOLS

    DEVTOOLS -.->|API calls| T1_STATUS

    style T1_STATUS fill:#009688,color:#fff
    style T2_STATUS fill:#0ea5e9,color:#fff
    style DEVTOOLS fill:#f59e0b,color:#fff
```

---

## 11. Environment Variables Security Flow

This diagram shows how environment variables are managed securely across local and production environments.

```mermaid
flowchart TD
    subgraph "Local Development"
        LOCAL_BE[Backend .env file<br/>OPENAI_API_KEY=sk-...]
        LOCAL_FE[Frontend .env.local file<br/>NEXT_PUBLIC_BACKEND_URL=localhost:8000]
        DOTENV["python-dotenv<br/>load_dotenv()"]
        NEXT_ENV[process.env in Next.js]
    end

    subgraph "Security Measures"
        GITIGNORE[.gitignore includes:<br/>.env<br/>.env.local]
        NEVER_COMMIT[NEVER commit<br/>.env files to Git!]
        ENV_EXAMPLE[.env.example for templates]
    end

    subgraph "Production (Vercel)"
        VERCEL_DASH[Vercel Dashboard]
        VERCEL_SETTINGS[Project Settings →<br/>Environment Variables]

        subgraph "Backend Env Vars"
            BE_KEY[OPENAI_API_KEY<br/>Stored securely in Vercel]
        end

        subgraph "Frontend Env Vars"
            FE_URL[NEXT_PUBLIC_BACKEND_URL<br/>Stored securely in Vercel]
        end
    end

    LOCAL_BE --> DOTENV
    DOTENV --> |os.getenv| LOCAL_BE
    LOCAL_FE --> NEXT_ENV
    NEXT_ENV --> |process.env| LOCAL_FE

    GITIGNORE -.->|Excludes| LOCAL_BE
    GITIGNORE -.->|Excludes| LOCAL_FE
    NEVER_COMMIT -.->|Warning!| LOCAL_BE
    ENV_EXAMPLE -.->|Template| LOCAL_BE

    VERCEL_DASH --> VERCEL_SETTINGS
    VERCEL_SETTINGS --> BE_KEY
    VERCEL_SETTINGS --> FE_URL

    style LOCAL_BE fill:#ef4444,color:#fff
    style LOCAL_FE fill:#ef4444,color:#fff
    style GITIGNORE fill:#22c55e,color:#fff
    style BE_KEY fill:#0ea5e9,color:#fff
    style FE_URL fill:#0ea5e9,color:#fff
    style NEVER_COMMIT fill:#ef4444,color:#fff
```

---

## 12. Integration Testing Workflow

This flowchart provides a decision-tree approach to testing the full-stack integration.

```mermaid
flowchart TD
    START([Start Integration Testing]) --> BE_TEST

    subgraph "Backend Testing"
        BE_TEST{Is backend running?}
        BE_TEST -->|No| BE_START[Start: uv run uvicorn<br/>api.index:app --reload]
        BE_TEST -->|Yes| BE_HEALTH[Check http://localhost:8000]
        BE_START --> BE_HEALTH

        BE_HEALTH --> BE_DOCS[Test /docs endpoint]
        BE_DOCS --> BE_API[Test /api/chat in Swagger]
        BE_API --> BE_SUCCESS{Backend works?}

        BE_SUCCESS -->|No| BE_DEBUG[Check:<br/>- OPENAI_API_KEY in .env<br/>- Port 8000 not in use<br/>- Dependencies installed]
        BE_DEBUG --> BE_TEST
        BE_SUCCESS -->|Yes| FE_TEST
    end

    subgraph "Frontend Testing"
        FE_TEST{Is frontend running?}
        FE_TEST -->|No| FE_START[Start: npm run dev]
        FE_TEST -->|Yes| FE_OPEN[Open http://localhost:3000]
        FE_START --> FE_OPEN

        FE_OPEN --> FE_LOAD{Page loads?}
        FE_LOAD -->|No| FE_DEBUG1[Check:<br/>- npm install completed<br/>- Port 3000 not in use<br/>- React versions match]
        FE_DEBUG1 --> FE_TEST

        FE_LOAD -->|Yes| FE_CONSOLE[Check browser console<br/>for errors]
        FE_CONSOLE --> INTEGRATION
    end

    subgraph "Integration Testing"
        INTEGRATION[Test Integration Features]
        INTEGRATION --> WISH_TEST[Submit a wish]
        WISH_TEST --> WISH_RESULT{Gets verdict?}

        WISH_RESULT -->|No| INT_DEBUG[Check:<br/>- NEXT_PUBLIC_BACKEND_URL set<br/>- Backend URL correct<br/>- Network tab shows API call<br/>- CORS errors?]
        INT_DEBUG --> INTEGRATION

        WISH_RESULT -->|Yes| CHAT_TEST[Send chat message]
        CHAT_TEST --> CHAT_RESULT{Gets AI response?}

        CHAT_RESULT -->|No| CHAT_DEBUG[Check:<br/>- /api/santa-chat route exists<br/>- Backend responds to /api/chat<br/>- Console shows backend URL]
        CHAT_DEBUG --> INTEGRATION

        CHAT_RESULT -->|Yes| SUCCESS
    end

    SUCCESS([Integration Successful!<br/>Ready to deploy])

    style START fill:#0ea5e9,color:#fff
    style SUCCESS fill:#22c55e,color:#fff
    style BE_SUCCESS fill:#f59e0b,color:#000
    style FE_LOAD fill:#f59e0b,color:#000
    style WISH_RESULT fill:#f59e0b,color:#000
    style CHAT_RESULT fill:#f59e0b,color:#000
```

---

## 13. Troubleshooting Decision Tree

This comprehensive decision tree helps diagnose and fix common integration issues.

```mermaid
flowchart TD
    PROBLEM([Integration Issue?]) --> TYPE{What's the symptom?}

    TYPE -->|Frontend can't reach backend| ENV_ISSUE
    TYPE -->|CORS errors| CORS_ISSUE
    TYPE -->|Backend returns 500| BE500_ISSUE
    TYPE -->|Port already in use| PORT_ISSUE
    TYPE -->|React version errors| REACT_ISSUE

    subgraph ENV_ISSUE["Environment Variable Issues"]
        ENV1{Local or Production?}
        ENV1 -->|Local| ENV_LOCAL[Check .env.local exists<br/>NEXT_PUBLIC_BACKEND_URL<br/>set correctly]
        ENV1 -->|Production| ENV_PROD[Check Vercel Dashboard<br/>Environment Variables set]

        ENV_LOCAL --> ENV2{Correct format?}
        ENV_PROD --> ENV2

        ENV2 -->|No trailing slash| ENV3[Remove trailing /<br/>from URL]
        ENV2 -->|Missing http://| ENV4[Add http:// or https://]
        ENV2 -->|Wrong port| ENV5[Use :8000 for local<br/>Vercel URL for prod]

        ENV3 --> ENV_RESTART[Restart dev servers]
        ENV4 --> ENV_RESTART
        ENV5 --> ENV_RESTART
        ENV_RESTART --> FIXED1([Fixed!])
    end

    subgraph CORS_ISSUE["CORS Errors"]
        CORS1["Check backend<br/>api/index.py"]
        CORS1 --> CORS2{CORS middleware exists?}

        CORS2 -->|No| CORS3["Add CORSMiddleware<br/>with allow_origins=['*']"]
        CORS2 -->|Yes| CORS4{allow_origins set?}

        CORS4 -->|Set to specific origin| CORS5["Change to ['*'] for dev<br/>or add frontend URL"]
        CORS3 --> CORS_RESTART[Restart backend]
        CORS5 --> CORS_RESTART
        CORS_RESTART --> FIXED2([Fixed!])
    end

    subgraph BE500_ISSUE["Backend 500 Errors"]
        BE500_1{Local or Production?}
        BE500_1 -->|Local| BE500_LOCAL[Check .env file<br/>OPENAI_API_KEY set]
        BE500_1 -->|Production| BE500_PROD[Check Vercel Dashboard<br/>OPENAI_API_KEY set]

        BE500_LOCAL --> BE500_2{Key format correct?}
        BE500_PROD --> BE500_2

        BE500_2 -->|Should start with sk-| BE500_3[Verify OpenAI API key<br/>at platform.openai.com]
        BE500_3 --> BE500_4[Restart backend or<br/>redeploy to Vercel]
        BE500_4 --> FIXED3([Fixed!])
    end

    subgraph PORT_ISSUE["Port Conflicts"]
        PORT1{Which port?}
        PORT1 -->|3000| PORT_FE["kill -9 $(lsof -ti tcp:3000)"]
        PORT1 -->|8000| PORT_BE["kill -9 $(lsof -ti tcp:8000)"]

        PORT_FE --> PORT_RESTART[Restart dev server]
        PORT_BE --> PORT_RESTART
        PORT_RESTART --> FIXED4([Fixed!])
    end

    subgraph REACT_ISSUE["React Version Mismatch"]
        REACT1[Open package.json]
        REACT1 --> REACT2{react and react-dom<br/>both 19.2.1?}

        REACT2 -->|No| REACT3[Edit package.json<br/>Set both to 19.2.1]
        REACT3 --> REACT4[Delete node_modules<br/>and package-lock.json]
        REACT4 --> REACT5[npm install<br/>--legacy-peer-deps]
        REACT5 --> FIXED5([Fixed!])

        REACT2 -->|Yes| REACT6[Check for conflicting<br/>@radix-ui versions]
        REACT6 --> REACT4
    end

    style FIXED1 fill:#22c55e,color:#fff
    style FIXED2 fill:#22c55e,color:#fff
    style FIXED3 fill:#22c55e,color:#fff
    style FIXED4 fill:#22c55e,color:#fff
    style FIXED5 fill:#22c55e,color:#fff
    style PROBLEM fill:#ef4444,color:#fff
```

---

## 14. Session Comparison: Progression from 1 to 3

This diagram shows how the three sessions build upon each other in technology, focus, and deployment complexity.

```mermaid
graph TB
    subgraph "Session 1: Frontend Basics"
        S1_TITLE[Session 1<br/>AI-Assisted Frontend Development]

        subgraph S1_TECH["Technology"]
            S1_T1[Next.js + React]
            S1_T2["v0.dev (AI UI generation)"]
            S1_T3[Tailwind CSS]
            S1_T4[shadcn/ui components]
        end

        subgraph S1_FOCUS["Learning Focus"]
            S1_F1[UI generation with AI]
            S1_F2[React component structure]
            S1_F3[Frontend deployment]
            S1_F4[No backend needed]
        end

        subgraph S1_DEPLOY["Deployment"]
            S1_D1[Vercel]
            S1_D2[Static/SSR Next.js]
            S1_D3[Single service]
        end
    end

    subgraph "Session 2: Backend Basics"
        S2_TITLE[Session 2<br/>Backend Development & LLM Integration]

        subgraph S2_TECH["Technology"]
            S2_T1[FastAPI + Python]
            S2_T2[OpenAI API]
            S2_T3[Uvicorn server]
            S2_T4[Pydantic validation]
        end

        subgraph S2_FOCUS["Learning Focus"]
            S2_F1[API endpoints]
            S2_F2[LLM integration]
            S2_F3[System prompts & personas]
            S2_F4[Backend deployment]
        end

        subgraph S2_DEPLOY["Deployment"]
            S2_D1[Vercel]
            S2_D2[Python serverless functions]
            S2_D3[Single service]
        end
    end

    subgraph "Session 3: Full-Stack Integration"
        S3_TITLE[Session 3<br/>Connecting Frontend to Backend]

        subgraph S3_TECH["Technology"]
            S3_T1[Next.js + FastAPI]
            S3_T2[API proxy routes]
            S3_T3[Environment variables]
            S3_T4[CORS middleware]
        end

        subgraph S3_FOCUS["Learning Focus"]
            S3_F1[Frontend ↔ Backend integration]
            S3_F2[Dual deployment strategy]
            S3_F3[Environment variable management]
            S3_F4[Full-stack debugging]
        end

        subgraph S3_DEPLOY["Deployment"]
            S3_D1["Vercel (both services)"]
            S3_D2[Frontend serverless]
            S3_D3[Backend serverless]
            S3_D4[Two services communicating]
        end
    end

    S1_TITLE --> S3_TITLE
    S2_TITLE --> S3_TITLE
    S1_TECH --> S3_TECH
    S2_TECH --> S3_TECH
    S1_DEPLOY --> S3_DEPLOY
    S2_DEPLOY --> S3_DEPLOY

    style S1_TITLE fill:#0ea5e9,color:#fff
    style S2_TITLE fill:#009688,color:#fff
    style S3_TITLE fill:#7c3aed,color:#fff
    style S3_DEPLOY fill:#22c55e,color:#fff
```

---

## 15. Quick Reference Tables

### Commands Table

| Task | Command |
|------|---------|
| **Backend Development** |
| Install uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Install backend dependencies | `cd app/backend-wish-list && uv sync` |
| Run backend server | `uv run uvicorn api.index:app --reload --port 8000` |
| Test backend health | `curl http://localhost:8000` |
| View API docs | `open http://localhost:8000/docs` |
| Kill backend port | `kill -9 $(lsof -ti tcp:8000)` |
| **Frontend Development** |
| Install frontend dependencies | `cd app/frontend-wish-list && npm install` |
| Run frontend dev server | `npm run dev` |
| Build frontend for production | `npm run build` |
| Run production build | `npm run start` |
| Lint frontend code | `npm run lint` |
| Kill frontend port | `kill -9 $(lsof -ti tcp:3000)` |
| Fix peer dependency issues | `npm install --legacy-peer-deps` |
| **Deployment** |
| Deploy backend to Vercel | `cd app/backend-wish-list && vercel --prod` |
| Deploy frontend to Vercel | `cd app/frontend-wish-list && vercel --prod` |
| View Vercel logs | `vercel logs [deployment-url]` |
| Add Vercel env variable | `vercel env add VAR_NAME production` |

### Endpoints Table

| Service | Method | Path | Purpose | Request Body | Response |
|---------|--------|------|---------|--------------|----------|
| **Backend** |
| Backend | GET | `/` | Health check | None | `{"status": "ok"}` |
| Backend | POST | `/api/chat` | Chat with St. Nicholas | `{"message": "..."}` | `{"reply": "..."}` |
| Backend | GET | `/docs` | Swagger UI | None | HTML page |
| Backend | GET | `/redoc` | ReDoc UI | None | HTML page |
| **Frontend API Routes** |
| Frontend | POST | `/api/santa-chat` | Proxy to backend `/api/chat` | `{"message": "..."}` | `{"reply": "..."}` |
| Frontend | POST | `/api/chat/single` | Wish evaluation (proxy) | `{"message": "..."}` | `{"reply": "..."}` |

### Environment Variables Table

| Variable | Service | Location | Value (Example) | Purpose |
|----------|---------|----------|-----------------|---------|
| `OPENAI_API_KEY` | Backend | `.env` (local)<br/>Vercel Dashboard (prod) | `sk-proj-abc123...` | Authenticate with OpenAI API |
| `NEXT_PUBLIC_BACKEND_URL` | Frontend | `.env.local` (local)<br/>Vercel Dashboard (prod) | `http://localhost:8000` (local)<br/>`https://backend.vercel.app` (prod) | Backend URL for API calls |

### File Checklist Table

| File | Location | Purpose | Must Edit? |
|------|----------|---------|------------|
| **Backend Files** |
| `api/index.py` | `app/backend-wish-list/` | FastAPI application | ✓ Yes |
| `pyproject.toml` | `app/backend-wish-list/` | Python project metadata | ✓ Yes |
| `requirements.txt` | `app/backend-wish-list/` | Vercel dependencies | ✓ Yes |
| `vercel.json` | `app/backend-wish-list/` | Vercel routing config | ✓ Yes |
| `.env` | `app/backend-wish-list/` | API keys (local) | ✓ Yes |
| `.gitignore` | `app/backend-wish-list/` | Ignore secrets | ✓ Yes |
| **Frontend Files** |
| `app/page.tsx` | `app/frontend-wish-list/` | Main wish list page | ✓ Yes (if customizing UI) |
| `app/api/santa-chat/route.ts` | `app/frontend-wish-list/` | Chat proxy to backend | ✓ Yes |
| `app/api/chat/single/route.ts` | `app/frontend-wish-list/` | Wish evaluation proxy | ✓ Yes |
| `package.json` | `app/frontend-wish-list/` | Dependencies | ✓ Yes (versions) |
| `next.config.ts` | `app/frontend-wish-list/` | Next.js configuration | Optional |
| `.env.local` | `app/frontend-wish-list/` | Environment variables (local) | ✓ Yes |
| `tsconfig.json` | `app/frontend-wish-list/` | TypeScript configuration | Optional |

---

*These diagrams are rendered using [Mermaid.js](https://mermaid.js.org/). View them in any Markdown viewer that supports Mermaid (GitHub, VS Code with extensions, Cursor IDE, etc.).*
