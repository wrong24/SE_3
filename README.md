# Virtual Software Engineering Lab

A comprehensive virtual laboratory for learning software engineering concepts through interactive exercises and simulations.

## Overview

This project provides hands-on experience with:

- Project Management tools and methodologies
- Collaboration tools and workflows
- Agile development practices
- Testing frameworks and methodologies

## Installation

1. Create and activate virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Project Structure

```
CC_VLab/
├── main_dashboard/        # Main application interface
├── project_management/    # PM exercises
│   ├── sdlc/
│   ├── wbs/
│   ├── gantt/
│   ├── resource_allocation/
│   └── risk_management/
├── collaboration_tools/   # Collaboration exercises
│   ├── git_flow/
│   ├── pr_merge/
│   ├── chat_sim/
│   ├── markdown_doc/
│   └── file_sharing/
├── agile_methodology/    # Agile practice exercises
│   ├── scrum_board/
│   ├── kanban/
│   ├── user_stories/
│   ├── sprint_planning/
│   └── burndown_chart/
├── testing_frameworks/   # Testing exercises
│   ├── unit_test/
│   ├── integration_test/
│   ├── tdd_sim/
│   ├── test_automation/
│   └── ci_cd/
└── backend_services/    # Core services
    ├── progress_tracker.py
    └── user_session.py
```

## Running the Application

1. Start all services using the provided script:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\start_services.ps1
```

2. Access the main dashboard at: `http://localhost:8000`

## Module Descriptions

### Project Management

- SDLC Visualization (Port: 8001)
- Work Breakdown Structure (Port: 8002)
- Gantt Chart Creation (Port: 8003)
- Resource Allocation (Port: 8004)
- Risk Management (Port: 8005)

### Collaboration Tools

- Git Flow Simulation (Port: 8006)
- PR & Merge Practice (Port: 8007)
- Chat Simulation (Port: 8008)
- Markdown Editor (Port: 8009)
- File Sharing (Port: 8010)

### Agile Methodology

- Scrum Board (Port: 8011)
- Kanban Board (Port: 8012)
- User Stories (Port: 8013)
- Sprint Planning (Port: 8014)
- Burndown Chart (Port: 8015)

### Testing Frameworks

- Unit Testing (Port: 8016)
- Integration Testing (Port: 8017)
- TDD Simulation (Port: 8018)
- Test Automation (Port: 8019)
- CI/CD Pipeline (Port: 8020)

## Accessing Database Data Through APIs

Each backend service exposes API endpoints to interact with its associated database (SQLite):

- **Progress Tracker:**

  - GET current progress: `http://localhost:9000/progress`
  - POST updates: `http://localhost:9000/progress`

- **User Session Service:**

  - Manage sessions: `http://localhost:9001/session`

- **Dashboard Backend:**
  - Main dashboard API: `http://localhost:9100/`

Use your browser or API tools (e.g., Postman) to send requests to these endpoints.

## Building and Running Containers

For each topic or service group:

1. Navigate into the folder (e.g., `Agile`) and run:
   ```bash
   docker-compose up --build
   ```
2. To run all services at once, use the top-level `docker-compose.yml` (if available) that includes all six services.

All containers are attached to a common network (`lab_network`), so they can communicate with one another if needed.

## Dependencies

- FastAPI: Backend API framework
- Streamlit: Frontend interface
- SQLite: Data persistence
- Plotly: Data visualization
- PyTest: Testing framework

For complete list, see `requirements.txt`

## Development

### Adding New Exercises

1. Create new directory under appropriate category
2. Implement backend.py and main.py
3. Add service to start_services.ps1
4. Update main dashboard

### Running Tests

```powershell
pytest
```

## Troubleshooting

1. Port conflicts:

   - Check if ports 8000-8020 are available
   - Modify port numbers in start_services.ps1 if needed

2. Database issues:
   - Delete .db files to reset
   - Check write permissions
