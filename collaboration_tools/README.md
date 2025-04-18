# Collaboration Tools Microservices

This folder contains services for collaboration exercises:

## Microservices Overview

### 1. Git Flow Simulation (Port: 8006)

#### Endpoint: View Branch Structure

- **URL:** `GET /branches`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "branches": [
      {
        "name": "string",
        "lastCommit": "string",
        "author": "string",
        "timestamp": "date"
      }
    ]
  }
  ```

---

### 2. PR & Merge Practice (Port: 8007)

#### Endpoint: Process Pull Requests

- **URL:** `POST /merge`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Body:**
  ```json
  {
    "sourceBranch": "string",
    "targetBranch": "string",
    "commitMessage": "string"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Merge successful",
    "mergedBranch": {
      "name": "string",
      "lastCommit": "string",
      "author": "string",
      "timestamp": "date"
    }
  }
  ```

---

### 3. Chat Simulation (Port: 8008)

#### Endpoint: Get Chat History

- **URL:** `GET /chat-history`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "messages": [
      {
        "sender": "string",
        "message": "string",
        "timestamp": "date"
      }
    ]
  }
  ```

---

### 4. Markdown Editor (Port: 8009)

#### Endpoint: Render Markdown Preview

- **URL:** `POST /preview`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Body:**
  ```json
  {
    "markdownText": "string"
  }
  ```
- **Response:**
  ```json
  {
    "htmlPreview": "string"
  }
  ```

---

### 5. File Sharing (Port: 8010)

#### Endpoint: List Shared Files

- **URL:** `GET /files`
- **Headers:**  
  `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "files": [
      {
        "fileName": "string",
        "fileSize": "number",
        "uploadedBy": "string",
        "uploadedAt": "date"
      }
    ]
  }
  ```

---

## Running the Services

To build and run all services:

```
docker build -t collab_service .
docker run -p 8006-8010:8006-8010 collab_service
```

Ensure all required environment variables are set for each service.
