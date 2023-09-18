FROM python:3.9-slim


USER root
RUN apt-get update
RUN apt-get install -y pkg-config
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y python3-dev
RUN apt-get install libssl-dev
RUN apt-get install -y build-essential
RUN apt-get install mariadb-client


# Switch to a non-root user
RUN useradd --uid 1000 benito && chown -R benito /app
RUN useradd --uid 1001 guess && chown -R guess /app
USER benito


# Create working folder and install dependencies
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the application contents
COPY conf/cred.json ./conf/
COPY data/vocabulary.sql /docker-entrypoint-initdb.d/
COPY src/ ./src/
COPY tests/ ./tests/


# Run the service
WORKDIR /app/src
CMD ["uvicorn", "web_app:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
