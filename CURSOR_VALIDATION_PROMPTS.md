# Cursor Validation Prompts - Quick Reference

> **Purpose**: Use these prompts in Cursor's Plan Mode to validate applications against updated `.cursor/rules/` standards and generate detailed completion plans.

---

## 🔧 Backend Validation Prompt

**Location**: `/backend-wish-list`
**Cursor Rules**: `global.mdc`, `api-design.mdc`, `ai-integration.mdc`, `git-workflow.mdc`

### Paste This in Cursor Plan Mode:

```
@.cursor/rules/global.mdc @.cursor/rules/api-design.mdc @.cursor/rules/ai-integration.mdc

# Validate Backend Application & Create Completion Plan

## Phase 1: Current State Validation

Review @api/index.py against cursor rules:

1. **Code Structure**
   - FastAPI setup per @api-design.mdc?
   - Pydantic models (ChatRequest, ChatResponse)?
   - CORS configured for frontend?
   - OpenAI client per @ai-integration.mdc?

2. **API Endpoint** (POST /api/chat)
   - RESTful conventions?
   - OpenAPI metadata (summary, description)?
   - Error handling (HTTPException)?
   - Response model structure?

3. **Environment & Dependencies**
   - .env.example with OPENAI_API_KEY?
   - pyproject.toml dependencies?
   - requirements.txt for Vercel?
   - vercel.json configuration?

4. **Code Quality per @global.mdc**
   - Type hints on all functions?
   - snake_case naming?
   - Proper error handling?
   - OpenAI usage patterns?

## Phase 2: Gap Analysis

Identify missing:
- Response models (ChatResponse?)
- OpenAPI documentation
- Type hints
- Error response types
- Production CORS settings

## Phase 3: Implementation Plan

Create ordered task list:
1. Add missing type hints
2. Define ChatResponse model
3. Add OpenAPI metadata
4. Improve error handling
5. Verify deployment config

## Phase 4: Prioritize (Critical → Low)

Rank all tasks by importance.

## Output Required

1. Validation summary with line numbers
2. Gap analysis
3. Ordered task list with code examples
4. Testing strategy
```

---

## ⚛️ Frontend Validation Prompt

**Location**: `/frontend-wish-list`
**Cursor Rules**: `global.mdc`, `component-design.mdc`, `api-integration.mdc`, `git-workflow.mdc`

### Paste This in Cursor Plan Mode:

```
@.cursor/rules/global.mdc @.cursor/rules/component-design.mdc @.cursor/rules/api-integration.mdc

# Validate Frontend Application & Create Completion Plan

## Phase 1: Current State Validation

Review @app/page.tsx and components:

1. **Component Architecture**
   - 'use client' usage per @component-design.mdc?
   - React hooks patterns (useState, useEffect)?
   - TypeScript interfaces for all data?
   - Component composition structure?

2. **API Integration**
   - fetch implementation per @api-integration.mdc?
   - NEXT_PUBLIC_BACKEND_URL from env?
   - Error handling patterns?
   - Loading state management?
   - Type-safe API calls?

3. **UI/UX**
   - Tailwind CSS per @global.mdc?
   - Responsive design?
   - Accessibility attributes?
   - Chat message display?

4. **State Management**
   - useState usage per @component-design.mdc?
   - No derived state anti-patterns?
   - useEffect cleanup?
   - Message history management?

5. **Environment**
   - .env.local setup?
   - .env.example exists?
   - Backend URL configured?

## Phase 2: Gap Analysis

Identify issues:
- Missing TypeScript types
- Improper 'use client' usage
- Incomplete error handling
- Missing loading states
- Hard-coded URLs
- Missing prop types
- Improper key usage

## Phase 3: Implementation Plan

Create tasks:
1. Define TypeScript interfaces
2. Improve API error handling
3. Add loading indicators
4. Extract custom hooks if needed
5. Refactor components
6. Add environment validation
7. Implement error boundaries

## Phase 4: Component Breakdown

For each file, specify:
- Current issues (with line numbers)
- Required changes
- @.cursor/rules/ pattern reference
- Testing steps

## Output Required

1. Validation summary per component
2. Architecture assessment
3. Gap analysis with specifics
4. File-by-file refactor plan
5. Testing strategy
6. Vercel deployment checklist
```

---

## 🔗 End-to-End Integration Prompt

**Use After**: Individual backend/frontend validations
**Location**: Either project directory

### Paste This in Cursor:

```
# End-to-End Application Integration Validation

## Context
- Backend: FastAPI at /backend-wish-list
- Frontend: Next.js at /frontend-wish-list
- Integration: POST /api/chat endpoint

## Phase 1: Contract Validation

1. **API Types Match?**
   - Backend ChatRequest = Frontend request type?
   - Backend ChatResponse = Frontend response type?
   - Error formats consistent?

2. **CORS Configuration**
   - Backend allows frontend origin?
   - Frontend handles CORS errors?

3. **Environment Variables**
   - Backend: OPENAI_API_KEY?
   - Frontend: NEXT_PUBLIC_BACKEND_URL?
   - Prod vs dev settings aligned?

4. **Error Handling**
   - Error format consistent?
   - HTTP status codes handled?
   - User-friendly messages?

## Phase 2: Test Plan

Create steps for:
1. Local testing (backend:8000, frontend:3000)
2. Deployment testing (Vercel)
3. Error scenario testing
4. CORS verification

## Output Required

1. Integration issues found
2. Deployment gaps
3. End-to-end test plan
4. Production readiness checklist
```

---

## 📋 How to Use

### Step 1: Backend Validation
1. Open `/backend-wish-list` in Cursor
2. Press `Cmd/Ctrl+L` for chat
3. Type `/plan` to enter Plan Mode
4. Copy & paste **Backend Validation Prompt**
5. Review plan, approve to execute

### Step 2: Frontend Validation
1. Open `/frontend-wish-list` in Cursor
2. Press `Cmd/Ctrl+L` for chat
3. Type `/plan` to enter Plan Mode
4. Copy & paste **Frontend Validation Prompt**
5. Review plan, approve to execute

### Step 3: Integration Validation
1. After both apps validated
2. Open either project
3. Copy & paste **End-to-End Prompt**
4. Review integration issues

---

## 🎯 Expected Outputs

### Backend Plan Should Include:
- ✅ Code quality assessment
- ✅ Missing component list
- ✅ Type hint improvements
- ✅ OpenAPI metadata additions
- ✅ Deployment verification steps

### Frontend Plan Should Include:
- ✅ Component architecture review
- ✅ TypeScript type definitions
- ✅ API integration improvements
- ✅ UX/UI enhancements
- ✅ Vercel deployment config

### Integration Plan Should Include:
- ✅ API contract validation
- ✅ CORS verification
- ✅ Environment variable checks
- ✅ End-to-end test scenarios

---

## 📚 Cursor Rules Reference

### Backend Rules
- **global.mdc**: Python/FastAPI conventions, type hints, async patterns
- **api-design.mdc**: Single endpoint patterns, Pydantic models, error handling
- **ai-integration.mdc**: OpenAI SDK usage, error handling, token tracking
- **git-workflow.mdc**: Conventional commits, branch naming

### Frontend Rules
- **global.mdc**: Next.js/React/TypeScript conventions, Tailwind CSS
- **component-design.mdc**: React hooks, client vs server components, props patterns
- **api-integration.mdc**: fetch API, type-safe calls, error handling, loading states
- **git-workflow.mdc**: Conventional commits, branch naming

---

## 🚀 Quick Start Commands

```bash
# Backend validation
cd /home/donbr/aie-onramp/app/backend-wish-list
# Open in Cursor, use backend prompt above

# Frontend validation
cd /home/donbr/aie-onramp/app/frontend-wish-list
# Open in Cursor, use frontend prompt above
```

---

## 💡 Pro Tips

1. **Always use Plan Mode first** - Review before executing changes
2. **Reference cursor rules** - Use `@.cursor/rules/filename.mdc` in prompts
3. **Start with validation** - Understand current state before planning
4. **Prioritize tasks** - Focus on Critical → High → Medium → Low
5. **Test incrementally** - Verify each change before moving to next

---

## 📖 Full Documentation

See `/home/donbr/.claude/plans/cursor-prompts-validation-plan.md` for:
- Detailed prompt explanations
- MCP context used (FastAPI, Next.js docs)
- Pattern references from cursor rules
- Expected outcomes per phase
- Component-by-component breakdown examples
