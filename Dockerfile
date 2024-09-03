FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV ENV_PATH=/app/config/.ENV

CMD ["python", "scripts/orchestrator.py"]