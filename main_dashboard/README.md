# Main Dashboard Service

This folder contains the main dashboard which aggregates microservice outputs:

## Microservices Overview

### 1. Dashboard API (Port: 8501)

#### Endpoint: Get Dashboard Overview

- **URL:** `GET /dashboard`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "status": "success",
    "services": [
      {
        "name": "string",
        "status": "string",
        "lastUpdated": "date"
      }
    ]
  }
  ```

#### Endpoint: Push Configuration Changes

- **URL:** `POST /update`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Body:**
  ```json
  {
    "configKey": "string",
    "configValue": "string"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Configuration updated successfully",
    "updatedConfig": {
      "configKey": "string",
      "configValue": "string"
    }
  }
  ```

---

## Running the Service

To build and run the service:

```
docker build -t dashboard_service .
docker run -p 8501:8501 dashboard_service
```

Ensure all required environment variables are set for the service.
