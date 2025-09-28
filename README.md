# bushido (武士道)
Bushido is a discipline-driven personal logging and analytics app. It helps you capture structured data about training, recovery, and daily activities while keeping the system minimal, extensible, and under your control.

The core philosophy:

* Structured tracking – Activities are logged as Units (lifting, cardio, recovery, etc.) with consistent, composable formats.

* Data integrity – Built with SQLAlchemy, repository/service layers, and strong test coverage to ensure correctness.

* Extensibility – A modular Python package that can scale from simple daily logs to dashboards, analytics, and AI-assisted insights.

Bushido follows a layered architecture:

* Domain layer – Pure Python dataclasses define Units and SubUnits.

* Repository layer – SQLAlchemy-backed persistence with clear session management.

* Service layer – Encapsulates workflows like parsing, logging, and mapping input to storage.

* Infra – Adapters for DB connection, testing utilities, and CLI integration.

Key technologies:

* Python 3.13+ with Poetry

* SQLAlchemy 2.x for ORM and DB management

* Pytest for testing (unit + integration)

* React as a frontend that can connect via FastAPI

This structure keeps the core clean and testable, while making it easy to extend into richer applications (dashboards, RAG/LLM integrations, etc.).
## Setup Backend
```
poetry install 
poetry run bushido
```

## Tests
```
poetry run pytest
```

## Setup Frontend
```
cd bushido/frontend
npm install
npm run dev
```
