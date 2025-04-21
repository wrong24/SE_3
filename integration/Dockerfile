# Use an official Python runtime as a parent image
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8022 8024 8026
RUN chmod +x start_services.sh
CMD ["./start_services.sh"]