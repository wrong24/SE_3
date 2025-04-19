import streamlit as st
import requests
import uuid

st.set_page_config(page_title="User Stories Exercise", layout="wide")
st.title("User Stories Exercise")

# Create new user story form
with st.form("new_story"):
    st.header("Create User Story")
    as_a = st.text_input("As a...")
    i_want = st.text_input("I want to...")
    so_that = st.text_input("So that...")
    
    st.subheader("Acceptance Criteria")
    criteria1 = st.text_input("Criterion 1")
    criteria2 = st.text_input("Criterion 2")
    criteria3 = st.text_input("Criterion 3")
    
    priority = st.selectbox("Priority", ["Must Have", "Should Have", "Could Have", "Won't Have"])
    
    if st.form_submit_button("Create Story"):
        story = {
            "id": str(uuid.uuid4())[:8],
            "as_a": as_a,
            "i_want": i_want,
            "so_that": so_that,
            "acceptance_criteria": [c for c in [criteria1, criteria2, criteria3] if c],
            "priority": priority,
            "status": "draft"
        }
        response = requests.post("http://agile_methodology:8013/story", json=story)
        if response.status_code == 200:
            st.success("User Story created!")

# Display stories
st.header("User Stories")
response = requests.get("http://agile_methodology:8013/stories")
if response.status_code == 200:
    stories = response.json()["stories"]
    for story in stories:
        with st.expander(f"Story: As a {story['as_a']}..."):
            st.write(f"**I want to:** {story['i_want']}")
            st.write(f"**So that:** {story['so_that']}")
            st.write("**Acceptance Criteria:**")
            for criterion in story['acceptance_criteria']:
                st.write(f"- {criterion}")
            st.write(f"**Priority:** {story['priority']}")
            st.write(f"**Status:** {story['status']}")

# Instructions and completion
st.sidebar.header("Instructions")
st.sidebar.write("""
1. Create user stories following the template
2. Add clear acceptance criteria
3. Prioritize stories
4. Review and refine stories
""")

if st.button("Complete Exercise"):
    response = requests.post("http://agile_methodology:8013/complete_exercise")
    if response.status_code == 200:
        st.success("Exercise completed!")
        st.markdown('[Return to Dashboard](http://main_services:8000)')