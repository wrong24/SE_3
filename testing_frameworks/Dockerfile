FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8016 8017 8018 8019 8020
RUN chmod +x start_services.sh
CMD ["./start_services.sh"]