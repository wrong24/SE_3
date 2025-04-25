import streamlit as st
import requests
import uuid

st.set_page_config(page_title="TDD Exercise", layout="wide")
st.title("Test-Driven Development")

# TDD stage selector
current_stage = st.radio(
    "Current TDD Stage",
    ["Red (Write Failing Test)", "Green (Make Test Pass)", "Refactor"],
    help="Select the current stage of TDD cycle"
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Test Code")
    test_code = st.text_area(
        "Write your test here",
        height=300,
        key="test_code"
    )

with col2:
    st.subheader("Implementation")
    implementation = st.text_area(
        "Write your implementation here",
        height=300,
        key="implementation"
    )

if st.button("Submit TDD Cycle"):
    stage_data = {
        "test_code": test_code,
        "implementation": implementation,
        "stage": current_stage.split()[0].lower()
    }
    response = requests.post(
        "http://testing_frameworks:8018/tdd/cycle",
        json=stage_data
    )
    if response.status_code == 200:
        st.success(f"TDD cycle recorded! Total cycles: {response.json()['cycle_count']}")

# Display TDD cycles
st.header("TDD Cycle History")
response = requests.get("http://testing_frameworks:8018/tdd/cycles")
if response.status_code == 200:
    cycles = response.json()["cycles"]
    for i, cycle in enumerate(cycles, 1):
        with st.expander(f"Cycle {i} - {cycle['stage'].upper()} Stage"):
            st.subheader("Test Code")
            st.code(cycle["test_code"], language="python")
            st.subheader("Implementation")
            st.code(cycle["implementation"], language="python")

# Instructions
with st.sidebar:
    st.header("TDD Cycle")
    st.markdown("""
    1. **Red**: Write a failing test
    2. **Green**: Write minimal code to pass
    3. **Refactor**: Improve code quality
    
    Complete at least 3 cycles to finish the exercise.
    """)

# Complete exercise button
if len(cycles) >= 3:
    if st.button("Complete Exercise"):
        response = requests.post("http://testing_frameworks:8018/complete_exercise")
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