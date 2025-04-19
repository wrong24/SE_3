import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Test Automation Exercise", layout="wide")
st.title("Test Automation Framework")

# Create test suite form
with st.form("create_suite"):
    st.header("Create Test Suite")
    suite_name = st.text_input("Suite Name")
    
    # Add tests dynamically
    tests = []
    test_count = st.number_input("Number of Tests", min_value=1, max_value=10, value=1)
    
    for i in range(test_count):
        col1, col2 = st.columns(2)
        with col1:
            test_name = st.text_input(f"Test {i+1} Name", key=f"test_name_{i}")
        with col2:
            test_type = st.selectbox(f"Test {i+1} Type", 
                                   ["Unit", "Integration", "UI"], 
                                   key=f"test_type_{i}")
        tests.append({"name": test_name, "type": test_type})
    
    schedule = st.selectbox("Schedule", ["Hourly", "Daily", "Weekly"])
    
    if st.form_submit_button("Create Suite"):
        suite = {
            "name": suite_name,
            "tests": tests,
            "schedule": schedule
        }
        response = requests.post("http://testing_frameworks:8019/suite", json=suite)
        if response.status_code == 200:
            st.success("Test suite created!")

# Display test results
st.header("Test Execution Results")
col1, col2 = st.columns(2)

with col1:
    # Test suite overview
    response = requests.get("http://testing_frameworks:8019/suites")
    if response.status_code == 200:
        suites = response.json()["suites"]
        if suites:
            for suite in suites:
                with st.expander(f"Suite: {suite['name']}"):
                    st.write(f"Schedule: {suite['schedule']}")
                    st.write(f"Total Tests: {len(suite['tests'])}")
                    
                    # Simulate test execution
                    if st.button("Run Suite", key=f"run_{suite['name']}"):
                        result = {
                            "suite_name": suite['name'],
                            "passed": len(suite['tests']) - 1,
                            "failed": 1,
                            "execution_time": 2.5
                        }
                        requests.post("http://testing_frameworks:8019/results", json=result)
                        st.success("Test suite executed!")

with col2:
    # Results visualization
    response = requests.get("http://testing_frameworks:8019/results")
    if response.status_code == 200:
        results = response.json()["results"]
        if results:
            df = pd.DataFrame(results)
            
            # Create pass/fail chart
            fig = px.bar(df, 
                        x="suite_name",
                        y=["passed", "failed"],
                        title="Test Results by Suite",
                        barmode="stack")
            st.plotly_chart(fig)

# Instructions
with st.sidebar:
    st.header("Instructions")
    st.markdown("""
    1. Create a test suite with multiple tests
    2. Configure execution schedule
    3. Run the suite manually
    4. Review test results and metrics
    5. Complete at least 3 test suite runs
    """)

# Complete exercise button
response = requests.get("http://testing_frameworks:8019/results")
if response.status_code == 200:
    results = response.json()["results"]
    if len(results) >= 3:
        if st.button("Complete Exercise"):
            response = requests.post("http://testing_frameworks:8019/complete_exercise")
            if response.status_code == 200:
                st.success("Exercise completed!")
                st.markdown('[Return to Dashboard](http://main_services:8000)')