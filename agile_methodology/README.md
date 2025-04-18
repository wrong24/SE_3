# Agile Methodology Services

This folder hosts microservices for Agile practices:

- **Scrum Board (Port: 8011):** Retrieve current sprint tasks via GET /tasks.
- **Kanban Board (Port: 8012):** POST /move to update task stages.
- **User Stories (Port: 8013):** GET /stories to list user stories.
- **Sprint Planning (Port: 8014):** POST /plan for sprint planning.
- **Burndown Chart (Port: 8015):** GET /burndown for progress visualization.

To run:

```
docker build -t agile_service .
docker run -p 8011-8015:8011-8015 agile_service
```
