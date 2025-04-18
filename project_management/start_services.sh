#!/bin/bash
uvicorn sdlc.backend:app --host 0.0.0.0 --port 8001 &
uvicorn wbs.backend:app --host 0.0.0.0 --port 8002 &
uvicorn gantt.backend:app --host 0.0.0.0 --port 8003 &
uvicorn resource_allocation.backend:app --host 0.0.0.0 --port 8004 &
uvicorn risk_management.backend:app --host 0.0.0.0 --port 8005 &
wait
