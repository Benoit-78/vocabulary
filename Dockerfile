FROM python:3.9-slim

USER root
RUN apt-get update
RUN apt-get install -y python3-tk
RUN apt-get install -y xvfb fontconfig

# Set the display environment variable to use Xvfb
ENV DISPLAY=:99
CMD ["Xvfb", ":99", "-screen", "0", "1024x768x16"]

# Create the fontconfig cache directories and set permissions
RUN mkdir -p /root/.cache/fontconfig && \
    chmod -R 755 /root/.cache/fontconfig && \
    fc-cache -f -v

# Create working folder and install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application contents
COPY data/ ./data/
COPY log/ ./log/
COPY src/ ./src/
COPY tests/ ./tests/

# Switch to a non-root user
RUN useradd --uid 1000 benito && chown -R benito /app
USER benito

# Run the service
EXPOSE 8080
ENTRYPOINT ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & python src/interro.py -t version -w 10 -r 2"]
# CMD ["python", "src/interro.py", "-t", "version", "-w", "10", "-r", "2"]