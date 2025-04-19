import streamlit as st
import requests
import json
import graphviz
from typing import List

st.set_page_config(page_title="Integration Testing Exercise", layout="wide")
st.title("Integration Testing Simulation")

# Initialize session state for test history
if 'test_history' not in st.session_state:
    st.session_state.test_history = []

# Get available services
response = requests.get("http://testing_frameworks:8017/services")
if response.status_code == 200:
    services = response.json()
    
    # Service Status Dashboard
    st.header("Service Status")
    cols = st.columns(len(services))
    for i, (service, details) in enumerate(services.items()):
        with cols[i]:
            status_color = "🟢" if details["status"] == "up" else "🔴"
            st.write(f"{status_color} {service.upper()}")
            st.write(f"Endpoint: {details['endpoint']}")

    # Service Flow Creation
    st.header("Create Integration Test")
    with st.form("test_flow"):
        # Service flow selection
        st.subheader("Service Flow")
        service_flow = st.multiselect(
            "Select services in order of execution",
            list(services.keys()),
            help="Select the services in the order they should be called"
        )
        
        # Expected result configuration
        st.subheader("Expected Result")
        col1, col2 = st.columns(2)
        with col1:
            expected_status = st.selectbox("Expected Status", ["success", "failure"])
        with col2:
            expected_code = st.number_input("Expected Response Code", min_value=200, max_value=500, value=200)
        
        expected_result = {
            "status": expected_status,
            "code": expected_code
        }
        
        if st.form_submit_button("Run Test"):
            test_case = {
                "service_flow": service_flow,
                "expected_result": expected_result
            }
            
            response = requests.post(
                "http://testing_frameworks:8017/test/integration",
                json=test_case
            )
            
            if response.status_code == 200:
                result = response.json()
                st.session_state.test_history.append(result)
                
                # Display result
                if result["success"]:
                    st.success("Integration test completed successfully!")
                else:
                    st.error("Integration test failed!")
                
                for message in result["results"]:
                    st.write(message)

# Visualize Service Flow
if service_flow:
    st.header("Service Flow Visualization")
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR')
    
    # Add nodes and edges
    for i, service in enumerate(service_flow):
        graph.node(service, service.upper())
        if i > 0:
            graph.edge(service_flow[i-1], service)
    
    st.graphviz_chart(graph)

# Test History
if st.session_state.test_history:
    st.header("Test History")
    for i, test in enumerate(st.session_state.test_history):
        with st.expander(f"Test Run {i + 1}"):
            st.write("**Service Flow:**", " → ".join(test["flow"]))
            st.write("**Results:**")
            for result in test["results"]:
                st.write(f"- {result}")
            st.write("**Status:**", "✅ Passed" if test["success"] else "❌ Failed")

# Instructions
with st.sidebar:
    st.header("Instructions")
    st.markdown("""
    1. **Create Test Flow:**
        - Select services in execution order
        - Define expected results
    
    2. **Run Tests:**
        - Execute integration tests
        - Verify service interactions
    
    3. **Analyze Results:**
        - Review test outcomes
        - Check service flow visualization
        - Monitor test history
    
    4. **Complete Exercise:**
        - Run at least 3 different test flows
        - Include both success and failure scenarios
    """)

# Complete exercise button
if len(st.session_state.test_history) >= 3:
    if st.button("Complete Exercise"):
        response = requests.post("http://testing_frameworks:8017/complete_exercise")
        if response.status_code == 200:
            st.success("Exercise completed!")
            st.markdown('[Return to Dashboard](http://main_services:8000)')