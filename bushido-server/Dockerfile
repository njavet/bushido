FROM python:3.14-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Workspace metadata first, for dependency-layer caching.
COPY pyproject.toml uv.lock ./
COPY bushidolib/pyproject.toml bushidolib/pyproject.toml
COPY bushido-server/pyproject.toml bushido-server/pyproject.toml

# Install dependencies without installing the actual project source yet.
RUN uv sync \
    --frozen \
    --package bushido-server \
    --no-install-workspace \
    --no-dev

# Now copy the source.
COPY bushidolib/ bushidolib/
COPY bushido-server/ bushido-server/

# Install the workspace packages themselves.
RUN uv sync \
    --frozen \
    --package bushido-server \
    --no-dev

ENV PATH="/app/.venv/bin:$PATH"

CMD ["server"]
