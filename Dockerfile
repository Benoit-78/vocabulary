FROM python:3.9-slim

USER root
RUN apt-get update

# Create working folder and install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application contents
COPY conf/cred.json ./conf/cred.json
COPY data/* ./data/*
COPY src/ ./src/
COPY tests/ ./tests/

# Switch to a non-root user
RUN useradd --uid 1000 benito && chown -R benito /app
USER benito

# Run the service
WORKDIR /app/src
CMD ["uvicorn", "routes:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
