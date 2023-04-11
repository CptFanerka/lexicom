FROM python:3.8-slim-buster
WORKDIR /lexicom
RUN apt-get update && apt-get -y install gcc libpq-dev
RUN apt-get install -y redis-server
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
