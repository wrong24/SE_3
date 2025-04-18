# Testing Frameworks Microservices

This folder hosts various testing exercises:

- **Unit Testing (Port: 8016):** GET /unit to run unit tests.
- **Integration Testing (Port: 8017):** POST /integration to trigger integration tests.
- **TDD Simulation (Port: 8018):** GET /tdd-status to check TDD state.
- **Test Automation (Port: 8019):** POST /automate to start automation suite.
- **CI/CD Pipeline (Port: 8020):** GET /pipeline to view CI/CD status.

To run:

```
docker build -t testing_service .
docker run -p 8016-8020:8016-8020 testing_service
```
