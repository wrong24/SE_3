#!/bin/bash
uvicorn git_flow.backend:app --host 0.0.0.0 --port 8006 &
uvicorn pr_merge.backend:app --host 0.0.0.0 --port 8007 &
uvicorn chat_sim.backend:app --host 0.0.0.0 --port 8008 &
uvicorn markdown_doc.backend:app --host 0.0.0.0 --port 8009 &
uvicorn file_share.backend:app --host 0.0.0.0 --port 8010 &
wait
