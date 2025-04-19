import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Scrum Board Exercise", layout="wide")

st.title("Scrum Board Exercise")

# Create new task form
with st.form("new_task"):
    st.header("Create New Task")
    title = st.text_input("Task Title")
    description = st.text_area("Description")
    points = st.number_input("Story Points", min_value=1, max_value=13)
    status = st.selectbox("Status", ["todo", "in_progress", "review", "done"])
    
    if st.form_submit_button("Create Task"):
        task = {
            "id": str(uuid.uuid4())[:8],
            "title": title,
            "description": description,
            "points": points,
            "status": status
        }
        response = requests.post("http://localhost:8011/task", json=task)
        if response.status_code == 200:
            st.success("Task created!")

# Display board
st.header("Scrum Board")
response = requests.get("http://localhost:8011/board")
if response.status_code == 200:
    board = response.json()
    
    cols = st.columns(4)
    for i, (status, tasks) in enumerate(board.items()):
        with cols[i]:
            st.subheader(status.upper())
            for task in tasks:
                with st.container():
                    st.write(f"**{task['title']}** ({task['points']} pts)")
                    st.write(task['description'])
                    new_status = st.selectbox(
                        "Move to",
                        ["todo", "in_progress", "review", "done"],
                        key=f"move_{task['id']}"
                    )
                    if new_status != task['status']:
                        response = requests.put(
                            f"http://localhost:8011/task/{task['id']}",
                            params={"new_status": new_status}
                        )
                        if response.status_code == 200:
                            st.experimental_rerun()
                    st.markdown("---")

# Complete exercise button
if st.button("Complete Exercise"):
    response = requests.post("http://localhost:8011/complete_exercise")
    if response.status_code == 200:
        st.success("Exercise completed! You can now move to the next topic.")
        st.markdown('[Return to Dashboard](http://localhost:8000)')

# Instructions sidebar
with st.sidebar:
    st.header("Instructions")
    st.write("""
    1. Create new tasks with story points
    2. Move tasks between different states
    3. Practice organizing work using Scrum board
    4. Complete the exercise when comfortable with Scrum concepts
    """)