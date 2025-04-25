import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import urllib.parse

st.set_page_config(page_title="Burndown Chart Exercise", layout="wide")
st.title("Burndown Chart Exercise")

# Restore session state from query params if present
query_params = st.query_params
if 'user_id' in query_params and 'start_time' in query_params:
    st.session_state['current_lab'] = {
        'user_id': query_params['user_id'][0],
        'start_time': query_params['start_time'][0]
    }

# Initialize sprint
with st.form("init_sprint"):
    st.header("Initialize Sprint")
    col1, col2 = st.columns(2)
    with col1:
        total_points = st.number_input("Total Story Points", min_value=1, value=50)
    with col2:
        duration_days = st.number_input("Sprint Duration (days)", min_value=1, value=14)
    
    if st.form_submit_button("Initialize Sprint"):
        response = requests.post(
            "http://localhost:8015/sprint/init",
            params={"total_points": total_points, "duration_days": duration_days}
        )
        if response.status_code == 200:
            st.success("Sprint initialized!")
            st.session_state.sprint_initialized = True

# Daily update form
with st.form("daily_update"):
    st.header("Daily Progress Update")
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date")
    with col2:
        points_completed = st.number_input("Points Completed Today", min_value=0)
    
    if st.form_submit_button("Update Progress"):
        response = requests.post(
            "http://localhost:8015/sprint/update",
            json={
                "date": date.strftime("%Y-%m-%d"),
                "points_completed": points_completed
            }
        )
        if response.status_code == 200:
            st.success("Progress updated!")

# Display burndown chart
st.header("Burndown Chart")
response = requests.get("http://localhost:8015/sprint/burndown")
if response.status_code == 200:
    sprint_data = response.json()
    
    if sprint_data["total_points"] > 0:
        # Create ideal burndown line
        ideal_data = pd.DataFrame({
            'day': range(sprint_data["duration_days"] + 1),
            'ideal': [sprint_data["total_points"] - (sprint_data["total_points"] / sprint_data["duration_days"]) * x 
                     for x in range(sprint_data["duration_days"] + 1)]
        })
        
        # Create actual burndown line
        actual_points = sprint_data["total_points"]
        actual_data = []
        for day, points in sprint_data["daily_progress"].items():
            actual_points -= points
            actual_data.append({
                'date': day,
                'remaining': actual_points
            })
        actual_df = pd.DataFrame(actual_data)
        
        # Create plotly figure
        fig = go.Figure()
        
        # Add ideal line
        fig.add_trace(go.Scatter(
            x=ideal_data['day'],
            y=ideal_data['ideal'],
            mode='lines',
            name='Ideal Burndown',
            line=dict(color='gray', dash='dash')
        ))
        
        # Add actual line if we have data
        if not actual_df.empty:
            fig.add_trace(go.Scatter(
                x=range(len(actual_df)),
                y=actual_df['remaining'],
                mode='lines+markers',
                name='Actual Burndown',
                line=dict(color='blue')
            ))
        
        fig.update_layout(
            title='Sprint Burndown Chart',
            xaxis_title='Sprint Day',
            yaxis_title='Story Points Remaining',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Points", sprint_data["total_points"])
        with col2:
            points_completed = sprint_data["total_points"] - actual_points if actual_data else 0
            st.metric("Points Completed", points_completed)
        with col3:
            st.metric("Points Remaining", actual_points if actual_data else sprint_data["total_points"])

# Instructions and completion
st.sidebar.header("Instructions")
st.sidebar.write("""
1. Initialize sprint parameters
2. Update daily progress
3. Monitor burndown trend
4. Compare actual vs ideal progress
5. Complete when comfortable with burndown charts
""")

if st.button("Complete Exercise"):
    response = requests.post("http://localhost:8015/complete_exercise")
    if response.status_code == 200:
        st.success("Exercise completed!")
        st.markdown('[Return to Dashboard](http://localhost:8000)')

if st.button("Return to Dashboard"):
    # Preserve session parameters when returning to dashboard
    current_lab = st.session_state.get("current_lab", {})
    user_id = current_lab.get("user_id", "")
    start_time = current_lab.get("start_time", "")
    params = urllib.parse.urlencode({"user_id": user_id, "start_time": start_time})
    st.switch_page(f"main.py?{params}")