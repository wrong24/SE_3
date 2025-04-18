# Virtual Software Engineering Lab

This project is a comprehensive virtual laboratory that leverages Docker to containerize multiple microservices for learning software engineering concepts through interactive exercises and simulations.

## Overview

The lab provides hands-on experience with the following microservices:

- **Project Management:** SDLC Visualization, Work Breakdown Structure, Gantt Chart Creation, Resource Allocation, Risk Management (Ports: 8001–8005)
- **Collaboration Tools:** Git Flow Simulation, PR & Merge Practice, Chat Simulation, Markdown Editor, File Sharing (Ports: 8006–8010)
- **Agile Methodology Services:** Scrum Board, Kanban Board, User Stories, Sprint Planning, Burndown Chart (Ports: 8011–8015)
- **Testing Frameworks:** Unit Testing, Integration Testing, TDD Simulation, Test Automation, CI/CD Pipeline (Ports: 8016–8020)
- **Main Dashboard:** Aggregates data from all microservices (Port: 8000)
- **Backend Services:** Progress Tracker, User Session Service, Dashboard API (Ports: 9000, 9001, 9100)

Each microservice has its own Dockerfile and README with detailed API endpoints and instructions.

## Project Structure

```
CC_VLab/
├── agile_methodology/     // Agile microservices (with Dockerfile and README.md)
├── collaboration_tools/   // Collaboration tools microservices (with Dockerfile and README.md)
├── testing_frameworks/    // Testing microservices (with Dockerfile and README.md)
├── project_management/    // Project management microservices (with Dockerfile and README.md)
├── main_dashboard/        // Main dashboard service (with Dockerfile and README.md)
└── backend_services/      // Backend core services (with Dockerfile and README.md)
```

## Prerequisites

- Docker installed on your system.
- Docker Compose installed.

## Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/wrong24/SE_3.git
   cd SE_3
   ```

2. Build and run all services using Docker Compose:

   ```bash
   docker-compose up --build
   ```

   This command builds Docker images for all services and starts all containers as defined in the docker-compose.yml file located in the root directory.

3. Alternatively, navigate into each service folder to build and run individually. For example, for Agile Methodology:
   ```bash
   cd agile_methodology
   docker build -t agile_service .
   docker run -p 8011-8015:8011-8015 agile_service
   ```

## Running the Application

- **Using Docker Compose:**  
  All microservices are orchestrated via the top-level docker-compose.yml. Upon running `docker-compose up --build`, every service (dashboard, backend, agile, collaboration, testing, project management) will start. The main dashboard (Port: 8000) aggregates data from each microservice.

- **Individual Service Details:**  
  Please refer to the README.md files within each service folder for specific API endpoints and usage instructions.

## API Endpoints Overview

### Main Dashboard (Port: 8000)

- GET /dashboard – Retrieve an overview of all microservice statuses.
- POST /update – Update dashboard configuration.

### Backend Services

- **Progress Tracker (Port: 9000):**
  - GET /progress – Retrieve current progress.
  - POST /progress – Update progress data.
- **User Session Service (Port: 9001):**
  - GET /session – Retrieve active sessions.
  - POST /session – Update session information.
- **Dashboard API (Port: 9100):**
  - GET / – Get consolidated data for dashboard display.

For details on API endpoints for Agile, Collaboration, Testing, and Project Management services, refer to their respective README.md files.

## Docker Compose Setup

The top-level docker-compose.yml (in the root folder) defines the configuration for all microservices, including network settings (using the common network `lab_network`). Running:

```bash
docker-compose up --build
```

will build and launch every service container.

## Troubleshooting

- Ensure all required ports (8000–8020, 9000, 9001, 9100) are available.
- Check service logs with:
  ```bash
  docker logs <container_name>
  ```
- Verify individual service endpoints as documented in each service's README.md.

## Contributing

Contributions are welcome. Please submit a pull request with a detailed description of your changes.

## License

[MIT License](LICENSE)

Enjoy exploring and learning with the Virtual Software Engineering Lab!
