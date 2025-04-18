FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8011 8012 8013 8014 8015
RUN chmod +x start_services.sh
CMD ["./start_services.sh"]
