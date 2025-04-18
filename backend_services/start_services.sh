#!/bin/bash
uvicorn progress_tracker:app --host 0.0.0.0 --port 9000 --reload &
uvicorn user_session:app --host 0.0.0.0 --port 9001 --reload & 
wait