
FROM python:3.11-slim-bullseye

RUN apt update -y && apt install --no-install-recommends awscli -y && apt upgrade -y && apt clean && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

CMD ["python3", "app.py"]