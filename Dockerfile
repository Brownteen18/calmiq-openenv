FROM python:3.10-slim

# Ensure Python output is sent straight to terminal
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port for the FastAPI environment
EXPOSE 7860

# We start uvicorn in the background (&) and then run inference.py
# The inference.py now has wait_for_server() to handle the delay
CMD uvicorn server.app:app --host 0.0.0.0 --port 7860 & python inference.py