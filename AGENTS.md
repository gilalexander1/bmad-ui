# Repository Guidelines

## Project Structure & Module Organization
- frontend/: Next.js 15 + TypeScript UI
  - src/app, src/components, globals.css, Tailwind/Next configs
- backend/: FastAPI API + WebSocket
  - main.py, agent_orchestrator.py, project_manager.py, websocket_manager.py
- docs/: Product and architecture notes
- docker-compose.yml: Local multi-service dev using mounted volumes

## Build, Test, and Development Commands
- Root full stack: `npm run full-dev` (Next.js + FastAPI with reload)
- Frontend dev: `npm run dev` • Build: `npm run build` • Start prod: `npm run start`
- Lint/types: `npm run lint` • `npm run type-check`
- Backend dev: `npm run backend-dev` (uvicorn reload) • One-off: `npm run backend`
- Docker: `docker-compose up --build` (uses NEXT_PUBLIC_API_URL/WS and backend env)

## Coding Style & Naming Conventions
- Frontend (TS/React):
  - Components: PascalCase in `frontend/src/components/*.tsx`; functions/vars camelCase.
  - Tailwind utility-first; prefer composable classes over custom CSS.
  - Run `npm run lint` and `type-check` before pushing. 2-space indent.
- Backend (Python):
  - PEP 8 with type hints; snake_case for funcs/vars, PascalCase for Pydantic models.
  - Keep module-level docstrings and concise, async-first endpoints.

## Testing Guidelines
- Current: No formal test suite. Required pre-PR checks: `npm run lint`, `npm run type-check`.
- Frontend (when adding tests): place `*.test.tsx` under `frontend/src/**/__tests__` or near components.
- Backend: prefer `pytest` + `httpx` client if introducing tests.
- Manual sanity: `GET /api/health`, `GET /api/system/status`, WebSocket `ws://localhost:8000/ws`.

## Commit & Pull Request Guidelines
- Commits: short, imperative, optionally emoji-prefixed (e.g., "🚀 Add workflow status panel").
- PRs: clear description, linked issues, screenshots for UI, API notes for backend, and steps to validate.
- Scope: small, focused changes; update docs when altering API, workflows, or agent behavior.

## Security & Configuration Tips
- Do not commit secrets. Use `.env` files; frontend reads `NEXT_PUBLIC_API_URL`/`NEXT_PUBLIC_WS_URL`; backend uses `CORS_ORIGINS`, `DEBUG`.
- Backend reads ecosystem data via mounted volumes (`.bmad-core`, `agents`, `infrastructure`). Avoid writing to these paths.
- Generated project data lives under `backend/projects_data/` (local dev artifacts).

## Agent/Ecosystem Notes
- Agents are orchestrated in `backend/agent_orchestrator.py`; ecosystem agents/templates are discovered by `BMADCoreIntegration` from the mounted paths. Prefer adding agents/templates in the ecosystem; mirror config locally only when necessary.
