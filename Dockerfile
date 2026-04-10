FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port (for FastAPI env if needed)
EXPOSE 7860

# 🚨 DO NOT HARDCODE ENV VARIABLES HERE

# Run inference
CMD ["python", "inference.py"]