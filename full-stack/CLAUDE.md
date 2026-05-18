# Full-Stack Development

## Structure
```
backend/
  python/     FastAPI or Flask projects
  java/       Spring Boot projects
frontend/
  react-typescript/  Vite + React + TypeScript
projects/
  <name>/     Combined full-stack apps with backend/ + frontend/
```

## Backend Conventions (Python)

- Framework: FastAPI (default) or Flask for smaller APIs
- Project layout:
  ```
  project_name/
    main.py           Entry point
    models/           Pydantic models / SQLAlchemy
    routes/           API route handlers
    services/         Business logic
    tests/            pytest
    requirements.txt
  ```
- Input validation at the boundary (Pydantic schemas)
- Proper HTTP status codes — no `200 OK` with error body
- Environment config via `.env` files, never hardcoded

## Backend Conventions (Java)

- Framework: Spring Boot
- Standard Maven/Gradle project layout
- Package by feature, not by layer
- Use Lombok for boilerplate reduction

## Frontend Conventions

- Vite + React + TypeScript
- Functional components with hooks
- Component co-location: `.tsx` + `.module.css` + `.test.tsx` in same dir
- State management: start with Context, add Zustand only when needed
- API calls extracted to a `services/` layer, not inline in components

## Project README
Each project must have a README with:
1. What it does (1-2 sentences)
2. How to run it (exact commands)
3. API endpoints or key screens
