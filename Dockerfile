FROM python:3.11-slim
# directorio
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "etl_pipeline.py"]