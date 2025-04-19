#!/bin/bash
uvicorn unit_test.backend:app --host 0.0.0.0 --port 8016 &
uvicorn integration_test.backend:app --host 0.0.0.0 --port 8017 &
uvicorn tdd_sim.backend:app --host 0.0.0.0 --port 8018 &
uvicorn test_automation.backend:app --host 0.0.0.0 --port 8019 &
uvicorn ci_cd.backend:app --host 0.0.0.0 --port 8020 &
wait
