FROM python:3.9-slim
WORKDIR /app
# ...existing code: copy dashboard files...
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "main.py"]
