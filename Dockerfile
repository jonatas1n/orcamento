FROM python:3.10

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    xvfb \
    libxi6 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3100
