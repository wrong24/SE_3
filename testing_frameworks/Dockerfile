FROM python:3.9-slim
WORKDIR /app
# ...existing code: copy testing framework files...
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8016 8017 8018 8019 8020
CMD ["python", "main.py"]
