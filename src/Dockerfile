# Using jdk 11 slim image to be able to run spark
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

# Workdir
WORKDIR /app

# Copy the requirements file
COPY src/requirements.txt .

RUN pip3.10 install --no-cache-dir -r requirements.txt

# Copy all the directories the API needs
COPY src/ /app/src/
COPY scripts/ /app/scripts/
COPY logs/ /app/logs
COPY models/ /app/models

# Expose the port the app runs on (flask)
EXPOSE 5000

# Run the API
CMD ["python3.10", "/app/src/app.py"]
