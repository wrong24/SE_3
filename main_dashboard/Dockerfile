FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501 9000 9001
COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]
