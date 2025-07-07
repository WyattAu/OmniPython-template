# Use independent of vscode devcontainer
# Builder stage
FROM python:3.11-slim as builder

# Install security updates
RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.8.2
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Install dependencies
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

# Copy and install application
COPY src/ ./src
RUN poetry build && pip install dist/*.whl

# Runtime stage
FROM python:3.11-slim as runtime

# Security hardening
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && mkdir /app && chown appuser:appuser /app

# Copy virtual environment
COPY --from=builder /root/.cache /root/.cache
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Run as non-root user
USER appuser
WORKDIR /app

# Application entrypoint
ENTRYPOINT ["python", "-m", "package_name"]
