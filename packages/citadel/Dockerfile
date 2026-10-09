FROM python:3.14-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy workspace metadata
COPY pyproject.toml uv.lock ./

# Copy packages required by the workspace
COPY packages/citadel ./packages/citadel
COPY alembic.ini /app/alembic.ini
COPY migrations /app/migrations

# Install Citadel and its dependencies
RUN uv sync \
    --frozen \
    --no-dev \
    --package citadel

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["server"]
