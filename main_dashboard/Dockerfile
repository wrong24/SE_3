FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY start.sh .
RUN chmod +x start.sh
EXPOSE 8000 9000 9001
CMD ["./start.sh"]
