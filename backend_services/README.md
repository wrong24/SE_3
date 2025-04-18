# Backend Services

This folder provides core backend functionalities:

## Microservices Overview

### 1. Progress Tracker Service (Port: 9000)

#### Endpoint: Retrieve Current Progress

- **URL:** `GET /progress`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "userId": "string",
    "completedTopics": ["string"],
    "quizScores": [
      {
        "topicId": "string",
        "score": "number",
        "completedAt": "date"
      }
    ]
  }
  ```

#### Endpoint: Update Progress

- **URL:** `POST /progress`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Body:**
  ```json
  {
    "userId": "string",
    "topicId": "string",
    "quizScore": "number"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Progress updated successfully",
    "updatedProgress": {
      "topicId": "string",
      "score": "number",
      "completedAt": "date"
    }
  }
  ```

---

### 2. User Session Service (Port: 9001)

#### Endpoint: Get Session Details

- **URL:** `GET /session`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "userId": "string",
    "sessionId": "string",
    "isActive": "boolean",
    "lastActiveAt": "date"
  }
  ```

#### Endpoint: Update Session

- **URL:** `POST /session`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Body:**
  ```json
  {
    "userId": "string",
    "isActive": "boolean"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Session updated successfully",
    "sessionDetails": {
      "userId": "string",
      "sessionId": "string",
      "isActive": "boolean",
      "lastActiveAt": "date"
    }
  }
  ```

---

### 3. Dashboard Backend Service (Port: 9100)

#### Endpoint: Get Consolidated Dashboard View

- **URL:** `GET /`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "userId": "string",
    "progress": {
      "completedTopics": ["string"],
      "quizScores": [
        {
          "topicId": "string",
          "score": "number",
          "completedAt": "date"
        }
      ]
    },
    "session": {
      "sessionId": "string",
      "isActive": "boolean",
      "lastActiveAt": "date"
    }
  }
  ```

---

## Running the Services

To build and run all services:

```
docker build -t backend_service .
docker run -p 9000-9001,9100:9000-9001,9100 backend_service
```

Ensure all required environment variables are set for each service.
