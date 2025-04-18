#!/bin/bash
uvicorn backend:app --host 0.0.0.0 --port 9100 --reload &
python -m streamlit run main.py --server.port 8000
