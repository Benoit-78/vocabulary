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
RUN useradd --uid 1000 benito && chown -R benito /app
RUN useradd --uid 1001 guess && chown -R guess /app


# Create working folder and install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt


# Copy the application contents
COPY conf/cred.json ./conf/cred.json
COPY conf/columns.json ./conf/columns.json
COPY data/zhongwen.sql /docker-entrypoint-initdb.d/zhongwen.sql
COPY src/ ./src/


# Run the service
# WORKDIR /app/src
WORKDIR /app
CMD uvicorn web:app --reload --host 0.0.0.0 --port 80
