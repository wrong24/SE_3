# Main Dashboard Service

This folder contains the main dashboard which aggregates microservice outputs:

- **Dashboard API (Port: 8000):**
  - GET /dashboard for an overview of service statuses.
  - POST /update to push configuration changes.
- Interconnects with other microservices by retrieving their data.

To run:

```
docker build -t dashboard_service .
docker run -p 8000:8000 dashboard_service
```
