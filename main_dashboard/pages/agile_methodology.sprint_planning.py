import streamlit as st
import requests
import uuid
from datetime import datetime, timedelta

st.set_page_config(page_title="Sprint Planning Exercise", layout="wide")
st.title("Sprint Planning Exercise")

# Sprint initialization
with st.form("init_sprint"):
    st.header("Initialize Sprint")
    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("Sprint Start Date")
    with col2:
        duration = st.number_input("Sprint Duration (days)", min_value=1, value=14)
    with col3:
        capacity = st.number_input("Sprint Capacity (points)", min_value=1, value=50)
    
    if st.form_submit_button("Initialize Sprint"):
        response = requests.post(
            "http://agile_methodology:8014/sprint/init",
            params={
                "start_date": start_date.strftime("%Y-%m-%d"),
                "duration": duration,
                "capacity": capacity
            }
        )
        if response.status_code == 200:
            st.success("Sprint initialized!")

# Add story to sprint
with st.form("add_story"):
    st.header("Add Story to Sprint")
    title = st.text_input("Story Title")
    points = st.number_input("Story Points", min_value=1, max_value=13)
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    assigned_to = st.text_input("Assign To")
    
    if st.form_submit_button("Add to Sprint"):
        story = {
            "id": str(uuid.uuid4())[:8],
            "title": title,
            "points": points,
            "priority": priority,
            "assigned_to": assigned_to
        }
        response = requests.post("http://agile_methodology:8014/sprint/add-story", json=story)
        if response.status_code == 200:
            st.success("Story added to sprint!")
        elif response.status_code == 400:
            st.error("Exceeds sprint capacity!")

# Display sprint details
st.header("Sprint Overview")
response = requests.get("http://agile_methodology:8014/sprint")
if response.status_code == 200:
    sprint = response.json()
    if sprint["start_date"]:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Sprint Duration", f"{sprint['end_date']} days")
        with col2:
            st.metric("Capacity", f"{sprint['capacity']} points")
        with col3:
            st.metric("Allocated", f"{sprint['allocated_points']} points")
        
        st.subheader("Sprint Backlog")
        for story in sprint["stories"]:
            with st.container():
                st.write(f"**{story['title']}** ({story['points']} pts)")
                st.write(f"Assigned to: {story['assigned_to']}")
                st.write(f"Priority: {story['priority']}")
                st.markdown("---")

# Instructions and completion
st.sidebar.header("Instructions")
st.sidebar.write("""
1. Initialize sprint parameters
2. Add stories within capacity
3. Assign team members
4. Review sprint workload
""")

if st.button("Complete Exercise"):
    response = requests.post("http://agile_methodology:8014/complete_exercise")
    if response.status_code == 200:
        st.success("Exercise completed!")
        st.markdown('[Return to Dashboard](http://main_services:8000)')