FROM python:3.9-slim
WORKDIR /app
# ...existing code: copy collaboration tool files...
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8006 8007 8008 8009 8010
CMD ["python", "main.py"]
