FROM python:3.12.2

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8001

CMD ["python", "kafka_client.py"] && ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]