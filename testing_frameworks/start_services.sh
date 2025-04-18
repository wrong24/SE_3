#!/bin/bash
uvicorn unit_testing.backend:app --host 0.0.0.0 --port 8016 &
uvicorn integration_testing.backend:app --host 0.0.0.0 --port 8017 &
uvicorn performance_testing.backend:app --host 0.0.0.0 --port 8018 &
uvicorn test_automation.backend:app --host 0.0.0.0 --port 8019 &
uvicorn test_reporting.backend:app --host 0.0.0.0 --port 8020 &
wait
