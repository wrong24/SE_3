# Backend Services

This folder provides core backend functionalities:

- **Progress Tracker (Port: 9000):**
  - GET /progress to retrieve current progress.
  - POST /progress to update progress.
- **User Session Service (Port: 9001):**
  - GET /session for session details.
  - POST /session to update sessions.
- **Dashboard Backend (Port: 9100):**
  - GET / for a consolidated view used by the main dashboard.

To run:

```
docker build -t backend_service .
docker run -p 9000-9001,9100:9000-9001,9100 backend_service
```
