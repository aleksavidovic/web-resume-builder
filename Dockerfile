# ---- Base Stage ----
FROM python:3.12-slim AS base

# Set environment variables for Python and Flask
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=wsgi:app

# Set the working directory
WORKDIR /app

# Install uv globally in the base image for access in all subsequent stages
RUN pip install uv

# ---- Builder Stage ----
# This stage compiles the dependencies into a requirements.txt file
FROM base AS builder

# Install system build dependencies, including postgresql-client for psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy only the necessary files for dependency resolution
COPY pyproject.toml uv.lock ./

# Generate requirements.txt using uv
RUN uv pip compile pyproject.toml -o requirements.txt

# ---- Runner Stage ----
# This is the final, small production image
FROM base AS runner

# Create a non-root user for security
RUN addgroup --system app && adduser --system --group app

# Install system runtime dependencies for WeasyPrint and PostgreSQL
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-xlib-2.0-0 \
    libffi-dev \
    shared-mime-info \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the generated requirements.txt from the builder stage
COPY --from=builder /app/requirements.txt .

# Install Python dependencies using uv pip sync for maximum speed
RUN uv pip sync --system --no-cache requirements.txt
#
# Create a cache directory and set ownership for the app user
RUN mkdir -p /home/app/.cache/fontconfig && \
    chown -R app:app /home/app

# Set the HOME environment variable so fontconfig knows where to look
ENV HOME=/home/app

# Copy the rest of the application code
COPY ./resume_builder ./resume_builder
COPY wsgi.py .
COPY entrypoint.sh .
COPY ./migrations ./migrations

# Change ownership of the app directory to the non-root user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port the app will run on
EXPOSE 8000

# Set the entrypoint to run the startup script
ENTRYPOINT ["./entrypoint.sh"]
