# Project Management Microservices

This folder offers microservices for project management:

- **SDLC Visualization (Port: 8001):** GET /sdlc for system development lifecycle details.
- **Work Breakdown Structure (Port: 8002):** GET /wbs to retrieve task breakdown.
- **Gantt Chart Creation (Port: 8003):** POST /gantt to create charts.
- **Resource Allocation (Port: 8004):** GET /resources for allocation info.
- **Risk Management (Port: 8005):** GET /risks to list project risks.

To run:

```
docker build -t pm_service .
docker run -p 8001-8005:8001-8005 pm_service
```
