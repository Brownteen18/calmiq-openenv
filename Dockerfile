FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

# ✅ BETTER PROCESS HANDLING
CMD ["sh", "-c", "uvicorn server.app:app --host 0.0.0.0 --port 7860 & sleep 5 && python inference.py"]