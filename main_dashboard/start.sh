#!/bin/bash
uvicorn file_share.backend:app --host 0.0.0.0 --port 9100 --reload &
python -m streamlit run main.py
