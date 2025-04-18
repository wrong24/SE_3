FROM python:3.9-slim
WORKDIR /app
# ...existing code: copy backend service files...
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 9000 9001 9100
CMD ["python", "start_backend.py"]
