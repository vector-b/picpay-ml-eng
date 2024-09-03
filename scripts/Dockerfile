# Orchestrator Dockerfile
FROM openjdk:11-slim

# Install dependencies to compile Python 3.10
RUN apt-get update && \
    apt-get install -y build-essential wget libssl-dev zlib1g-dev libncurses5-dev \
    libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev \
    liblzma-dev curl ant && \
    apt-get clean

# Download and install Python 3.10
RUN wget https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz && \
    tar -xf Python-3.10.12.tgz && \
    cd Python-3.10.12 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.10.12 Python-3.10.12.tgz

# Get pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.10 get-pip.py && \
    rm get-pip.py

# Define the JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
RUN export JAVA_HOME

# Workdir :)    
WORKDIR /app

# copy all directories api needs
COPY scripts /app/scripts
COPY data /app/data  
COPY logs /app/logs

# Install requirements
COPY requirements.txt ./
RUN pip3.10 install --no-cache-dir -r requirements.txt

# Define the environment variable for the .env file
ENV ENV_PATH=/app/config/.env

# Run orchestrator
CMD ["python3.10", "scripts/orchestrator.py"]
