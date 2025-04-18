FROM python:3.9-slim
WORKDIR /app
# ...existing code: copy project management files...
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8001 8002 8003 8004 8005
CMD ["python", "main.py"]
