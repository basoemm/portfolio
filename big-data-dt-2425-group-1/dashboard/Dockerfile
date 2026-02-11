############################
# 1. Build-time image
############################
FROM python:3.11-slim AS base

# Prevents Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System packages required for pandas, MySQL etc.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential gcc libmariadb-dev curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ————— install Python deps first (layer-cache friendly)
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install st-pages

############################
# 2. Runtime image
############################
FROM python:3.11-slim

# Copy the virtual env from the build stage
COPY --from=base /usr/local /usr/local
ENV PYTHONPATH=/app

WORKDIR /app
COPY . .

# Streamlit picks port 8501 by default
EXPOSE 8501

# Entry-point: run dashboard
CMD ["streamlit", "run", "app.py", \
     "--server.port", "8501", "--server.address", "0.0.0.0"]
