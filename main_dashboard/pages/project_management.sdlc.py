import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(page_title="SDLC Visualization", layout="wide")
st.title("Software Development Life Cycle")

# Get SDLC phases
response = requests.get("http://project_management:8001/phases")
phases = response.json()

# Create visualization
fig = go.Figure(data=[
    go.Bar(
        x=[phase["name"] for phase in phases],
        y=[1 for _ in phases],
        marker_color=["green" if phase["status"] == "completed" else "lightgray" for phase in phases]
    )
])

fig.update_layout(
    title="SDLC Phases Progress",
    showlegend=False,
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# Phase details and interaction
for i, phase in enumerate(phases):
    with st.expander(f"{phase['name']} Phase"):
        st.write(phase["description"])
        if phase["status"] == "pending" and st.button(f"Complete {phase['name']}", key=f"phase_{i}"):
            response = requests.post(f"http://project_management:8001/update/{i}")
            if response.status_code == 200:
                st.success(f"{phase['name']} phase completed!")
                st.rerun()

if all(phase["status"] == "completed" for phase in phases):
    if st.button("Complete Exercise"):
        response = requests.post("http://project_management:8001/complete_exercise")
        if response.status_code == 200:
            st.success("Exercise completed!")
            st.markdown('[Return to Dashboard](http://main_services:8000)')