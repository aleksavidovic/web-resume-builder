FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv pip compile pyproject.toml -o requirements.txt

# Stage 2
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/requirements.txt .

RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-xlib-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/resume_builder ./resume_builder
COPY wsgi.py .
COPY entrypoint.sh .
COPY ./migrations ./migrations

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
