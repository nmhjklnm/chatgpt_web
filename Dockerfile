FROM python:3.11


WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

# CMD ["streamlit", "run", "main.py", "--server.port=8080"]
