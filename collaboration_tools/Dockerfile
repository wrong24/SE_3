FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8006 8007 8008 8009 8010
RUN chmod +x start_services.sh
CMD ["./start_services.sh"]