import streamlit as st
import requests
import uuid
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Resource Allocation Exercise", layout="wide")
st.title("Resource Allocation")

# Resource creation form
with st.form("new_resource"):
    st.header("Add Resource")
    resource_name = st.text_input("Resource Name")
    role = st.selectbox("Role", ["Developer", "Designer", "Tester", "Manager"])
    availability = st.number_input("Weekly Availability (hours)", min_value=1, max_value=40, value=40)
    
    if st.form_submit_button("Add Resource"):
        resource = {
            "id": str(uuid.uuid4())[:8],
            "name": resource_name,
            "role": role,
            "availability": availability,
            "assigned_tasks": []
        }
        response = requests.post("http://project_management:8004/resource", json=resource)
        if response.status_code == 200:
            st.success("Resource added!")
            st.rerun()

# Resource assignment form
response = requests.get("http://project_management:8004/resources")
if response.status_code == 200:
    resources = response.json()["resources"]
    if resources:
        st.header("Assign Resources")
        with st.form("assign_resource"):
            resource_id = st.selectbox(
                "Select Resource",
                options=[(r["id"], f"{r['name']} ({r['role']})") for r in resources],
                format_func=lambda x: x[1]
            )[0]
            
            task_name = st.text_input("Task Name")
            hours = st.number_input("Hours Required", min_value=1, max_value=40)
            
            if st.form_submit_button("Assign"):
                assignment = {
                    "resource_id": resource_id,
                    "task_name": task_name,
                    "hours_needed": hours
                }
                response = requests.post("http://project_management:8004/assign", json=assignment)
                if response.status_code == 200:
                    st.success("Assignment created!")
                    st.rerun()
                elif response.status_code == 400:
                    st.error("Resource overallocation!")

# Display resource utilization
response_assignments = requests.get("http://project_management:8004/assignments")
if response_assignments.status_code == 200:
    assignments = response_assignments.json()["assignments"]
    if assignments and resources:
        # Prepare data for visualization
        resource_usage = []
        for resource in resources:
            total_hours = sum(a["hours_needed"] for a in assignments 
                            if a["resource_id"] == resource["id"])
            resource_usage.append({
                "Resource": f"{resource['name']} ({resource['role']})",
                "Used Hours": total_hours,
                "Available Hours": resource["availability"]
            })
        
        df = pd.DataFrame(resource_usage)
        
        # Create bar chart
        fig = px.bar(df, x="Resource", y=["Used Hours", "Available Hours"],
                    title="Resource Utilization",
                    barmode="overlay")
        st.plotly_chart(fig)

        # Show assignments table
        st.header("Current Assignments")
        assignments_df = pd.DataFrame([
            {
                "Resource": next(r["name"] for r in resources if r["id"] == a["resource_id"]),
                "Task": a["task_name"],
                "Hours": a["hours_needed"]
            }
            for a in assignments
        ])
        st.dataframe(assignments_df)

# Complete exercise button
if len(resources) >= 3 and len(assignments) >= 5:
    if st.button("Complete Exercise"):
        response = requests.post("http://project_management:8004/complete_exercise")
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