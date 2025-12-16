# Cursor Validation & Planning Prompts

## Overview

These prompts are designed to leverage the updated `.cursor/rules/` files to validate the current state of both frontend and backend applications and create detailed implementation plans.

**MCP Context Used:**
- FastAPI documentation (/websites/fastapi_tiangolo) - 31,710 code snippets
- Next.js documentation (/websites/nextjs) - 9,372 code snippets
- React hooks best practices from PydanticAI chat app example

---

## Backend Application Cursor Prompt

### Context
The backend is a **minimal FastAPI application** with:
- Single file: `api/index.py` (50 lines)
- ONE endpoint: `POST /api/chat`
- Direct OpenAI SDK usage (gpt-4o-mini)
- St. Nicholas persona
- No database, no state management

### Cursor Rules Available
- `global.mdc` - FastAPI/Python best practices
- `api-design.mdc` - Single endpoint patterns
- `ai-integration.mdc` - OpenAI SDK usage
- `git-workflow.mdc` - Git conventions

### Validation & Planning Prompt for Backend

```
@.cursor/rules/global.mdc @.cursor/rules/api-design.mdc @.cursor/rules/ai-integration.mdc

# TASK: Validate Backend Application & Create Completion Plan

## Phase 1: Current State Validation

Review the current backend implementation against our cursor rules:

1. **Code Structure Analysis** (@api/index.py)
   - Verify FastAPI setup follows @api-design.mdc patterns
   - Check Pydantic models (ChatRequest, ChatResponse if exists)
   - Validate CORS configuration for frontend communication
   - Confirm OpenAI client initialization per @ai-integration.mdc

2. **API Endpoint Validation** (POST /api/chat)
   - Verify endpoint follows RESTful conventions
   - Check OpenAPI metadata (summary, description, responses)
   - Validate error handling patterns (HTTPException usage)
   - Confirm response model structure

3. **Environment Configuration**
   - Check .env.example exists with placeholder OPENAI_API_KEY
   - Verify python-dotenv is properly configured
   - Confirm API key validation before requests

4. **Dependencies & Deployment**
   - Review pyproject.toml dependencies
   - Verify requirements.txt exists for Vercel deployment
   - Check vercel.json serverless configuration

5. **Alignment with Cursor Rules**
   - Does code follow @global.mdc Python style conventions?
   - Are type hints present per @global.mdc standards?
   - Does error handling match @api-design.mdc patterns?
   - Is OpenAI integration aligned with @ai-integration.mdc?

## Phase 2: Identify Gaps & Issues

Based on validation, identify:
1. **Missing Components**
   - Response model (ChatResponse) if not defined
   - OpenAPI documentation metadata
   - Proper error response types
   - Health check endpoint metadata

2. **Code Quality Issues**
   - Missing type hints
   - Improper error handling
   - Hard-coded values
   - Non-compliant naming conventions

3. **Deployment Readiness**
   - Missing environment variable checks
   - Incomplete Vercel configuration
   - Missing CORS production settings

## Phase 3: Create Detailed Implementation Plan

Generate a step-by-step plan to:

1. **Improve Code Quality**
   - Add missing type hints per @global.mdc
   - Enhance error messages per @api-design.mdc
   - Add OpenAPI metadata to all endpoints
   - Improve logging if needed

2. **Add Missing Components**
   - Define ChatResponse Pydantic model
   - Add comprehensive error response types
   - Create .env.example if missing
   - Add API documentation strings

3. **Deployment Optimization**
   - Verify CORS allows frontend URL
   - Add environment variable validation
   - Ensure proper error responses for production

4. **Testing Recommendations**
   - Manual testing steps for /api/chat endpoint
   - Health check verification
   - Error scenario testing
   - CORS verification

## Phase 4: Prioritization

Rank tasks by:
1. **Critical** - Blocks deployment or core functionality
2. **High** - Improves reliability or code quality significantly
3. **Medium** - Nice-to-have improvements
4. **Low** - Optional enhancements

## Expected Output

Provide:
1. **Validation Summary** - Current state assessment
2. **Gap Analysis** - What's missing or needs improvement
3. **Implementation Plan** - Ordered list of tasks with descriptions
4. **File-by-File Changes** - Specific edits needed
5. **Testing Strategy** - How to verify each change

Use the patterns and examples from @.cursor/rules/ files as your reference.
```

---

## Frontend Application Cursor Prompt

### Context
The frontend is a **Next.js 14+ application** with:
- React 18+ with TypeScript
- Tailwind CSS styling
- Santa's Wish List chat interface
- Connects to backend `/api/chat` endpoint

### Cursor Rules Available
- `global.mdc` - Next.js/React/TypeScript conventions
- `component-design.mdc` - React component patterns
- `api-integration.mdc` - Backend API integration
- `git-workflow.mdc` - Git conventions

### Validation & Planning Prompt for Frontend

```
@.cursor/rules/global.mdc @.cursor/rules/component-design.mdc @.cursor/rules/api-integration.mdc

# TASK: Validate Frontend Application & Create Completion Plan

## Phase 1: Current State Validation

Review the current frontend implementation against our cursor rules:

1. **Component Architecture Analysis** (@app/page.tsx)
   - Verify 'use client' directive usage per @component-design.mdc
   - Check React hooks patterns (useState, useEffect)
   - Validate TypeScript type definitions for props and state
   - Review component composition and structure

2. **API Integration Validation**
   - Check fetch implementation against @api-integration.mdc
   - Verify environment variable usage (NEXT_PUBLIC_BACKEND_URL)
   - Validate error handling patterns
   - Confirm loading state management
   - Check TypeScript types for API requests/responses

3. **UI/UX Implementation**
   - Review Tailwind CSS usage per @global.mdc
   - Verify responsive design patterns
   - Check accessibility considerations
   - Validate chat message display logic

4. **State Management**
   - Review useState usage per @component-design.mdc
   - Check for derived state anti-patterns
   - Verify useEffect cleanup patterns
   - Validate message history management

5. **Environment Configuration**
   - Check .env.local setup
   - Verify .env.example exists
   - Confirm NEXT_PUBLIC_BACKEND_URL configuration

6. **Alignment with Cursor Rules**
   - TypeScript conventions per @global.mdc?
   - Component patterns per @component-design.mdc?
   - API integration per @api-integration.mdc?
   - Proper use of client vs server components?

## Phase 2: Identify Gaps & Issues

Based on validation, identify:

1. **Component Structure Issues**
   - Missing TypeScript interfaces
   - Improper 'use client' usage
   - Anti-patterns in hooks usage
   - Missing error boundaries

2. **API Integration Gaps**
   - Missing type definitions for API responses
   - Incomplete error handling
   - Missing loading states
   - No retry logic or timeout handling
   - Hard-coded backend URLs

3. **Code Quality Issues**
   - Missing prop types
   - Improper key usage in lists
   - Inline styles instead of Tailwind
   - Missing accessibility attributes

4. **State Management Problems**
   - Storing derived state
   - Missing cleanup in useEffect
   - Race conditions in API calls
   - Memory leaks

## Phase 3: Create Detailed Implementation Plan

Generate a step-by-step plan to:

1. **Improve Type Safety**
   - Define all TypeScript interfaces per @global.mdc
   - Add proper types for ChatMessage, Wish, etc.
   - Type all API request/response functions
   - Add type guards where needed

2. **Enhance API Integration**
   - Implement proper error handling per @api-integration.mdc
   - Add loading states for all async operations
   - Create reusable API client utility
   - Add abort controller for race conditions
   - Implement environment variable checks

3. **Refactor Components**
   - Extract custom hooks if needed (useChat pattern)
   - Separate concerns (presentation vs logic)
   - Implement proper key management
   - Add error boundaries for resilience

4. **Improve UX**
   - Add loading indicators
   - Implement error messages
   - Add empty states
   - Ensure responsive design
   - Add accessibility attributes

5. **Production Readiness**
   - Configure environment variables for Vercel
   - Add error logging
   - Implement CORS error handling
   - Add connection status indicator

## Phase 4: Prioritization

Rank tasks by:
1. **Critical** - Breaks functionality or prevents deployment
2. **High** - Significant UX or reliability issues
3. **Medium** - Code quality and maintainability
4. **Low** - Nice-to-have enhancements

## Phase 5: Component-by-Component Breakdown

For each component file, specify:
1. **Current Issues** - What's wrong or missing
2. **Required Changes** - Specific code modifications
3. **Pattern Reference** - Which @.cursor/rules/ example to follow
4. **Testing Steps** - How to verify the fix

## Expected Output

Provide:
1. **Validation Summary** - Current state with specific line numbers
2. **Architecture Assessment** - Component structure analysis
3. **Gap Analysis** - Missing features or patterns
4. **Implementation Plan** - Ordered tasks with code examples
5. **File-by-File Refactor Plan** - Specific changes per file
6. **Testing Strategy** - Manual and automated testing steps
7. **Deployment Checklist** - Vercel-specific configurations

Reference patterns and examples from @.cursor/rules/ files throughout.
```

---

## Combined End-to-End Validation Prompt

### For Cross-Application Validation

```
# TASK: End-to-End Application Validation

## Context
- **Backend**: FastAPI app at /backend-wish-list
- **Frontend**: Next.js app at /frontend-wish-list
- **Integration**: Frontend calls backend POST /api/chat endpoint

## Phase 1: Integration Validation

1. **API Contract Validation**
   - Backend ChatRequest model matches frontend request type?
   - Backend ChatResponse model matches frontend response type?
   - Error response formats are consistent?

2. **CORS Configuration**
   - Backend allows frontend origin?
   - Frontend handles CORS errors gracefully?

3. **Environment Variables**
   - Backend: OPENAI_API_KEY configured?
   - Frontend: NEXT_PUBLIC_BACKEND_URL configured?
   - Production vs development settings aligned?

4. **Error Handling Consistency**
   - Backend error format matches frontend expectations?
   - HTTP status codes properly handled in frontend?
   - Error messages user-friendly?

## Phase 2: Create Integration Test Plan

1. **Local Testing**
   - Start backend on port 8000
   - Start frontend on port 3000
   - Test chat flow end-to-end
   - Verify error scenarios

2. **Deployment Testing**
   - Verify Vercel environment variables
   - Test deployed backend health check
   - Test deployed frontend connection
   - Verify CORS in production

## Expected Output

1. **Integration Issues** - Mismatches between frontend/backend
2. **Deployment Gaps** - Missing configurations
3. **End-to-End Test Plan** - Step-by-step testing guide
4. **Production Readiness Checklist** - All deployment requirements
```

---

## Usage Instructions

### For Backend (Plan Mode)

1. Open `/home/donbr/aie-onramp/app/backend-wish-list` in Cursor
2. Enter Plan Mode (Cmd/Ctrl+L → Type `/plan`)
3. Copy the **Backend Validation & Planning Prompt**
4. Paste and submit
5. Review generated plan before executing

### For Frontend (Plan Mode)

1. Open `/home/donbr/aie-onramp/app/frontend-wish-list` in Cursor
2. Enter Plan Mode (Cmd/Ctrl+L → Type `/plan`)
3. Copy the **Frontend Validation & Planning Prompt**
4. Paste and submit
5. Review generated plan before executing

### For End-to-End Validation

1. Use after both individual validations
2. Open either project in Cursor
3. Copy the **Combined End-to-End Validation Prompt**
4. Review integration issues
5. Create unified testing plan

---

## Key Patterns to Reference

### Backend Patterns (from cursor rules)
- **Error Handling**: HTTPException with status codes
- **Type Hints**: All function signatures typed
- **OpenAI Usage**: Direct SDK calls, no frameworks
- **Environment Config**: python-dotenv with validation

### Frontend Patterns (from cursor rules)
- **Type Safety**: TypeScript interfaces for all data
- **Hooks**: useState for state, useEffect with cleanup
- **API Calls**: fetch with error handling, loading states
- **Components**: 'use client' only when needed
- **Styling**: Tailwind CSS classes, no inline styles

---

## Expected Outcomes

After running these prompts in Plan Mode, you should have:

1. **Backend**:
   - Complete validation report
   - List of code quality improvements
   - API documentation enhancements
   - Deployment readiness checklist
   - Prioritized task list

2. **Frontend**:
   - Component-by-component analysis
   - TypeScript type improvements
   - API integration enhancements
   - UX/UI refinements
   - Production deployment plan

3. **Integration**:
   - Contract validation results
   - CORS configuration verification
   - End-to-end testing strategy
   - Deployment coordination plan

All outputs should reference specific patterns from the `.cursor/rules/` files, ensuring consistency with established standards.
