# Project Management Microservices

This folder offers microservices for project management:

## Microservices Overview

### 1. SDLC Visualization Service (Port: 8001)

#### Endpoint: Get SDLC Details

- **URL:** `GET /sdlc`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "phases": [
      {
        "name": "string",
        "description": "string",
        "startDate": "date",
        "endDate": "date"
      }
    ]
  }
  ```

---

### 2. Work Breakdown Structure Service (Port: 8002)

#### Endpoint: Retrieve Task Breakdown

- **URL:** `GET /wbs`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "tasks": [
      {
        "id": "string",
        "name": "string",
        "parentTaskId": "string",
        "status": "string"
      }
    ]
  }
  ```

---

### 3. Gantt Chart Creation Service (Port: 8003)

#### Endpoint: Create Gantt Chart

- **URL:** `POST /gantt`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Body:**
  ```json
  {
    "tasks": [
      {
        "id": "string",
        "name": "string",
        "startDate": "date",
        "endDate": "date",
        "dependencies": ["string"]
      }
    ]
  }
  ```
- **Response:**
  ```json
  {
    "message": "Gantt chart created successfully",
    "chartId": "string"
  }
  ```

---

### 4. Resource Allocation Service (Port: 8004)

#### Endpoint: Get Resource Allocation Info

- **URL:** `GET /resources`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "resources": [
      {
        "id": "string",
        "name": "string",
        "allocatedTo": "string",
        "availability": "string"
      }
    ]
  }
  ```

---

### 5. Risk Management Service (Port: 8005)

#### Endpoint: List Project Risks

- **URL:** `GET /risks`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "risks": [
      {
        "id": "string",
        "description": "string",
        "severity": "string",
        "mitigationPlan": "string"
      }
    ]
  }
  ```

---

## Running the Services

To build and run all services:

```
docker build -t pm_service .
docker run -p 8001-8005:8001-8005 pm_service
```

Ensure all required environment variables are set for each service.
