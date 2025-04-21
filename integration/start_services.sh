#!/bin/bash
uvicorn analytics_tracker:app --host 0.0.0.0 --port 8022 &
uvicorn progress_tracker:app --host 0.0.0.0 --port 8024 &
uvicorn user_managment:app --host 0.0.0.0 --port 8026 &
wait
