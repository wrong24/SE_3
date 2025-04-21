import streamlit as st
import requests
import uuid
import plotly.graph_objects as go
import networkx as nx

st.set_page_config(page_title="Work Breakdown Structure", layout="wide")
st.title("Work Breakdown Structure (WBS)")

# Initialize tasks as empty list
tasks = []

# First try to get existing tasks
try:
    response = requests.get("http://project_management:8002/tasks/")
    if response.status_code == 200:
        tasks = response.json().get("tasks", [])
except requests.exceptions.RequestException as e:
    st.warning(f"Could not connect to backend: {e}")

# Task creation form
with st.form("new_task"):
    st.header("Add Task")
    task_name = st.text_input("Task Name")
    duration = st.number_input("Duration (days)", min_value=1, value=1)
    parent_task = st.selectbox(
        "Parent Task",
        ["None"] + [task["name"] for task in tasks]
    )
    
    if st.form_submit_button("Add Task"):
        task = {
            "id": str(uuid.uuid4())[:8],
            "name": task_name,
            "duration": duration,
            "parent_id": None if parent_task == "None" else next((t["id"] for t in tasks if t["name"] == parent_task), None)
        }
        try:
            response = requests.post("http://project_management:8002/task/", json=task)
            if response.status_code == 200:
                st.success("Task added!")
                st.rerun()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to add task: {e}")

# Display WBS if we have tasks
if tasks:
    # Create network graph
    G = nx.DiGraph()
    for task in tasks:
        G.add_node(task["name"])
        if task["parent_id"]:
            parent_name = next((t["name"] for t in tasks if t["id"] == task["parent_id"]), None)
            if parent_name:
                G.add_edge(parent_name, task["name"])
    
    pos = nx.spring_layout(G)
    
    # Create Plotly figure
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)

    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode='markers+text',
        text=[node for node in G.nodes()],
        textposition="bottom center",
        marker=dict(size=20)
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=0, l=0, r=0, t=0),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                   ))

    st.plotly_chart(fig, use_container_width=True)

    # Complete exercise button
    if len(tasks) >= 5:
        if st.button("Complete Exercise"):
            try:
                response = requests.post("http://project_management:8002/complete_exercise")
                if response.status_code == 200:
                    st.success("Exercise completed!")
                    st.markdown('[Return to Dashboard](http://main_services:8000)')
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to complete exercise: {e}")
else:
    st.info("No tasks found. Add some tasks to see the Work Breakdown Structure.")