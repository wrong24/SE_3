import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Version Control Exercise", layout="wide")

st.title("Version Control Simulation")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0

def create_commit(branch: str, message: str):
    response = requests.post(
        "http://localhost:8006/commit",
        json={
            "message": message,
            "branch": branch,
            "hash": str(uuid.uuid4())[:8]
        }
    )
    new_hash = str(uuid.uuid4())[:8]
    return {"message": "Commit successful", "hash": new_hash}

def create_branch(name: str, base: str):
    response = requests.post(
        "http://localhost:8006/create-branch",
        json={"name": name, "base": base}
    )
    return response.json()

def merge_branches(source: str, target: str):
    response = requests.post(
        "http://localhost:8006/merge",
        params={"source": source, "target": target}
    )
    return response.json()

# Git Flow Exercise Steps
steps = [
    {
        "title": "Create Feature Branch",
        "description": "Create a new feature branch from develop",
        "action": lambda: create_branch("feature/new-feature", "develop")
    },
    {
        "title": "Make Changes",
        "description": "Commit changes to your feature branch",
        "action": lambda: create_commit("feature/new-feature", "Add new feature")
    },
    {
        "title": "Merge to Develop",
        "description": "Merge your feature branch into develop",
        "action": lambda: merge_branches("feature/new-feature", "develop")
    },
    {
        "title": "Release",
        "description": "Merge develop into main for release",
        "action": lambda: merge_branches("develop", "main")
    }
]

# Display current repository state
if st.button("Refresh Repository State"):
    response = requests.get("http://localhost:8006/state")
    if response.status_code == 200:
        state = response.json()
        st.json(state)

# Display current step
if st.session_state.step < len(steps):
    current_step = steps[st.session_state.step]
    st.header(f"Step {st.session_state.step + 1}: {current_step['title']}")
    st.write(current_step['description'])
    
    if st.button("Execute Step"):
        result = current_step['action']()
        msg = result.get("message", "Operation completed")
        st.success(f"Step completed: {msg}")
        st.session_state.step += 1

# Complete exercise button
if st.session_state.step >= len(steps):
    if st.button("Complete Exercise"):
        response = requests.post("http://localhost:8006/complete_exercise")
        if response.status_code == 200:
            st.success("Exercise completed! You can now move to the next topic.")
            st.markdown('[Return to Dashboard](http://localhost:8000)')

# Instructions sidebar
with st.sidebar:
    st.header("Instructions")
    st.write("""
    This exercise simulates Git Flow workflow:
    1. Create a feature branch
    2. Make changes and commit
    3. Merge feature into develop
    4. Release to main
    
    Follow each step and observe the repository state.
    """)