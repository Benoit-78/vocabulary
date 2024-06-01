FROM python:3.9-slim


USER root
RUN apt-get update
RUN apt-get install -y pkg-config
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y python3-dev
RUN apt-get install libssl-dev
RUN apt-get install -y build-essential
RUN apt-get install -y mariadb-client


# Switch to a non-root user
WORKDIR /app
RUN useradd --uid 1000 developer && chown -R developer /app


# Create working folder and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# Copy the application contents
COPY src/ ./src/


# Run the service
CMD uvicorn src.web:app --reload --host 0.0.0.0 --port 80
