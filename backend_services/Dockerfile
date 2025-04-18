FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 9000 9001 9100
RUN chmod +x start_services.sh
CMD ["./start_services.sh"]