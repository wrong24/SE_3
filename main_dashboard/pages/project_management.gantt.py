import streamlit as st
import requests
import uuid
import plotly.figure_factory as ff
from datetime import datetime, timedelta

st.set_page_config(page_title="Gantt Chart Exercise", layout="wide")
st.title("Gantt Chart Creation")

# Task creation form
with st.form("new_task"):
    st.header("Add Task")
    task_name = st.text_input("Task Name")
    start_date = st.date_input("Start Date")
    duration = st.number_input("Duration (days)", min_value=1, value=1)
    
    # Get existing tasks for dependencies
    response = requests.get("http://project_management:8003/tasks")
    existing_tasks = response.json().get("tasks", [])
    dependencies = st.multiselect(
        "Dependencies",
        options=[task["name"] for task in existing_tasks]
    )
    
    if st.form_submit_button("Add Task"):
        task = {
            "id": str(uuid.uuid4())[:8],
            "name": task_name,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "duration": duration,
            "dependencies": dependencies,
            "progress": 0
        }
        response = requests.post("http://project_management:8003/task", json=task)
        if response.status_code == 200:
            st.success("Task added!")
            st.rerun()

# Display Gantt chart
response = requests.get("http://project_management:8003/tasks")
if response.status_code == 200:
    tasks = response.json()["tasks"]
    if tasks:
        # Prepare data for Gantt chart
        df = []
        for task in tasks:
            start = datetime.strptime(task["start_date"], "%Y-%m-%d")
            finish = start + timedelta(days=task["duration"])
            df.append(dict(
                Task=task["name"],
                Start=start,
                Finish=finish,
                Progress=task["progress"]
            ))
        
        fig = ff.create_gantt(df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Task progress update
        st.header("Update Task Progress")
        for task in tasks:
            col1, col2 = st.columns([3, 1])
            with col1:
                progress = st.slider(
                    f"Progress for {task['name']}",
                    0, 100, task["progress"],
                    key=f"progress_{task['id']}"
                )
            with col2:
                if st.button("Update", key=f"update_{task['id']}"):
                    response = requests.put(
                        f"http://project_management:8003/task/{task['id']}",
                        params={"progress": progress}
                    )
                    if response.status_code == 200:
                        st.success("Progress updated!")
                        st.rerun()

# Complete exercise button
if len(tasks) >= 3 and all(task["progress"] == 100 for task in tasks):
    if st.button("Complete Exercise"):
        response = requests.post("http://project_management:8003/complete_exercise")
        if response.status_code == 200:
            st.success("Exercise completed!")
            st.markdown('[Return to Dashboard](http://main_services:8000)')

if st.button("Return to Dashboard"):
    current_lab = st.session_state.get("current_lab", {})
    st.session_state["session_params"] = {
        "user_id": current_lab.get("user_id", ""),
        "start_time": current_lab.get("start_time", "")
    }
    st.switch_page("main.py")