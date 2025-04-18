# Agile Methodology Services

This folder hosts microservices for Agile practices:

## Microservices Overview

### 1. Scrum Board Service (Port: 8011)

#### Endpoint: Retrieve Current Sprint Tasks

- **URL:** `GET /tasks`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "tasks": [
      {
        "id": "string",
        "title": "string",
        "status": "string",
        "assignee": "string"
      }
    ]
  }
  ```

---

### 2. Kanban Board Service (Port: 8012)

#### Endpoint: Update Task Stages

- **URL:** `POST /move`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Body:**
  ```json
  {
    "taskId": "string",
    "newStage": "string"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Task moved successfully",
    "updatedTask": {
      "id": "string",
      "title": "string",
      "status": "string",
      "assignee": "string"
    }
  }
  ```

---

### 3. User Stories Service (Port: 8013)

#### Endpoint: List User Stories

- **URL:** `GET /stories`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "stories": [
      {
        "id": "string",
        "title": "string",
        "description": "string",
        "priority": "string"
      }
    ]
  }
  ```

---

### 4. Sprint Planning Service (Port: 8014)

#### Endpoint: Plan Sprint

- **URL:** `POST /plan`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Body:**
  ```json
  {
    "sprintName": "string",
    "startDate": "date",
    "endDate": "date",
    "tasks": ["string"]
  }
  ```
- **Response:**
  ```json
  {
    "message": "Sprint planned successfully",
    "sprintDetails": {
      "id": "string",
      "name": "string",
      "startDate": "date",
      "endDate": "date",
      "tasks": ["string"]
    }
  }
  ```

---

### 5. Burndown Chart Service (Port: 8015)

#### Endpoint: Get Burndown Chart Data

- **URL:** `GET /burndown`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "sprintId": "string",
    "chartData": [
      {
        "date": "date",
        "remainingTasks": "number"
      }
    ]
  }
  ```

---

## Running the Services

To build and run all services:

```
docker build -t agile_service .
docker run -p 8011-8015:8011-8015 agile_service
```

Ensure all required environment variables are set for each service.
