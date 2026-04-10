FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

# Start API server (HF-compatible entrypoint)
CMD ["python", "/app/inference.py"]