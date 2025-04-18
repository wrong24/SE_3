import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="CI/CD Pipeline Exercise", layout="wide")
st.title("CI/CD Pipeline Configuration")

# Create pipeline form
with st.form("create_pipeline"):
    st.header("Create Pipeline")
    pipeline_name = st.text_input("Pipeline Name")
    
    # Configure stages
    st.subheader("Pipeline Stages")
    stages = st.multiselect(
        "Select Stages",
        ["Build", "Test", "Security Scan", "Deploy to Staging", "Deploy to Production"],
        ["Build", "Test"]
    )
    
    # Configure tests
    st.subheader("Test Configuration")
    col1, col2 = st.columns(2)
    with col1:
        unit_tests = st.checkbox("Unit Tests", value=True)
        integration_tests = st.checkbox("Integration Tests")
    with col2:
        e2e_tests = st.checkbox("E2E Tests")
        performance_tests = st.checkbox("Performance Tests")
    
    # Configure deployment
    st.subheader("Deployment Configuration")
    deployment_type = st.selectbox("Deployment Type", ["Blue-Green", "Rolling", "Canary"])
    auto_rollback = st.checkbox("Enable Auto-rollback")
    
    if st.form_submit_button("Create Pipeline"):
        pipeline = {
            "name": pipeline_name,
            "stages": stages,
            "tests": {
                "unit": unit_tests,
                "integration": integration_tests,
                "e2e": e2e_tests,
                "performance": performance_tests
            },
            "deployment": {
                "type": deployment_type,
                "auto_rollback": auto_rollback
            }
        }
        response = requests.post("http://localhost:8020/pipeline", json=pipeline)
        if response.status_code == 200:
            st.success("Pipeline created!")

# Display pipelines and runs
st.header("Pipeline Overview")
col1, col2 = st.columns([2, 3])

with col1:
    # Pipeline list
    response = requests.get("http://localhost:8020/pipelines")
    if response.status_code == 200:
        pipelines = response.json()["pipelines"]
        if pipelines:
            for pipeline in pipelines:
                with st.expander(f"Pipeline: {pipeline['name']}"):
                    st.write("**Stages:**")
                    for stage in pipeline['stages']:
                        st.write(f"- {stage}")
                    
                    st.write("\n**Tests:**")
                    for test, enabled in pipeline['tests'].items():
                        st.write(f"- {test}: {'✅' if enabled else '❌'}")
                    
                    st.write("\n**Deployment:**")
                    st.write(f"Type: {pipeline['deployment']['type']}")
                    st.write(f"Auto-rollback: {'✅' if pipeline['deployment']['auto_rollback'] else '❌'}")
                    
                    if st.button("Run Pipeline", key=f"run_{pipeline['name']}"):
                        response = requests.post(
                            "http://localhost:8020/run",
                            params={"pipeline_name": pipeline['name']}
                        )
                        if response.status_code == 200:
                            st.success("Pipeline started!")

with col2:
    # Pipeline runs visualization
    response = requests.get("http://localhost:8020/runs")
    if response.status_code == 200:
        runs = response.json()["runs"]
        if runs:
            df = pd.DataFrame(runs)
            
            # Create status chart
            fig = px.bar(df, 
                        x="pipeline_name",
                        color="status",
                        title="Pipeline Runs Status")
            st.plotly_chart(fig)

# Instructions
with st.sidebar:
    st.header("Instructions")
    st.markdown("""
    1. Create a CI/CD pipeline
    2. Configure pipeline stages
    3. Set up test requirements
    4. Configure deployment strategy
    5. Run the pipeline at least once
    """)

# Complete exercise button
response = requests.get("http://localhost:8020/runs")
if response.status_code == 200:
    runs = response.json()["runs"]
    if len(runs) >= 1:
        if st.button("Complete Exercise"):
            response = requests.post("http://localhost:8020/complete_exercise")
            if response.status_code == 200:
                st.success("Exercise completed!")
                st.markdown('[Return to Dashboard](http://localhost:8000)')