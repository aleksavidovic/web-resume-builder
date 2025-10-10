# ---- Base Stage ----
FROM python:3.12-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=wsgi:app

# Set the working directory
WORKDIR /app

# ---- Builder Stage ----
FROM base AS builder

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Generate requirements.txt from uv.lock
RUN uv pip compile pyproject.toml -o requirements.txt

# ---- Runner Stage ----
FROM base AS runner

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Install runtime dependencies for WeasyPrint
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-xlib-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt from the builder stage and install packages
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./resume_builder ./resume_builder
COPY wsgi.py .
COPY entrypoint.sh .
COPY ./migrations ./migrations

# Change ownership of the app directory
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port Gunicorn will run on
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]
