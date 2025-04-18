# Collaboration Tools Microservices

This folder contains services for collaboration exercises:

- **Git Flow Simulation (Port: 8006):** GET /branches to view branch structure.
- **PR & Merge Practice (Port: 8007):** POST /merge to process pull requests.
- **Chat Simulation (Port: 8008):** GET /chat-history for messages.
- **Markdown Editor (Port: 8009):** POST /preview to render markdown.
- **File Sharing (Port: 8010):** GET /files to list shared files.

To run:

```
docker build -t collab_service .
docker run -p 8006-8010:8006-8010 collab_service
```
