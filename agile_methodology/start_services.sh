#!/bin/bash
uvicorn burndown_chart.backend:app --host 0.0.0.0 --port 8015 &
uvicorn kanban.backend:app --host 0.0.0.0 --port 8012 &
uvicorn scrum_board.backend:app --host 0.0.0.0 --port 8011 &
uvicorn sprint_planning.backend:app --host 0.0.0.0 --port 8014 &
uvicorn user_stories.backend:app --host 0.0.0.0 --port 8013 &
wait
