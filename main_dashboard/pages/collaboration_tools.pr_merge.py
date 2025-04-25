import streamlit as st
import requests
import json

st.set_page_config(page_title="Pull Request & Merge Exercise", layout="wide")

st.title("Pull Request & Merge Exercise")

# Initialize session state
if 'current_pr' not in st.session_state:
    st.session_state.current_pr = None

# Create PR Form
st.header("Create Pull Request")
with st.form("pr_form"):
    title = st.text_input("PR Title")
    description = st.text_area("PR Description")
    code_changes = st.text_area("Code Changes", 
                               value="""def calculate_sum(a, b):
    # TODO: Add input validation
    return a + b + 1  # Fixed the calculation""")
    
    submit_pr = st.form_submit_button("Create PR")
    
    if submit_pr and title and description:
        response = requests.post(
            "http://collaboration_tools:8007/create-pr",
            json={
                "title": title,
                "description": description,
                "source_branch": "feature/fix-calculation",
                "target_branch": "main",
                "changes": code_changes
            }
        )
        if response.status_code == 200:
            st.success("Pull Request created successfully!")
            st.session_state.current_pr = response.json()["pr_id"]

# Display PRs
st.header("Pull Requests")
response = requests.get("http://collaboration_tools:8007/list-prs")
if response.status_code == 200:
    prs = response.json()["pull_requests"]
    for pr in prs:
        with st.expander(f"{pr['title']} (#{pr['id']}) - {pr['status']}"):
            st.write(f"**Description:** {pr['description']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original Code")
                response = requests.get("http://collaboration_tools:8007/code/main")
                if response.status_code == 200:
                    st.code(response.json()["code"], language="python")
            
            with col2:
                st.subheader("Proposed Changes")
                st.code(pr["changes"], language="python")
            
            if pr["status"] == "open":
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Approve", key=f"approve_{pr['id']}"):
                        response = requests.post(
                            f"http://collaboration_tools:8007/review-pr/{pr['id']}",
                            params={"approve": True}
                        )
                        if response.status_code == 200:
                            st.success("PR approved and merged!")
                            st.rerun()
                
                with col2:
                    if st.button("Reject", key=f"reject_{pr['id']}"):
                        response = requests.post(
                            f"http://collaboration_tools:8007/review-pr/{pr['id']}",
                            params={"approve": False}
                        )
                        if response.status_code == 200:
                            st.error("PR rejected!")
                            st.rerun()

# Complete exercise button
if st.button("Complete Exercise"):
    response = requests.post("http://collaboration_tools:8007/complete_exercise")
    if response.status_code == 200:
        st.success("Exercise completed! You can now move to the next topic.")
        st.markdown('[Return to Dashboard](http://main_services:8000)')

if st.button("Return to Dashboard"):
    current_lab = st.session_state.get("current_lab", {})
    st.session_state["session_params"] = {
        "user_id": current_lab.get("user_id", ""),
        "start_time": current_lab.get("start_time", "")
    }
    st.switch_page("main.py")

# Instructions sidebar
with st.sidebar:
    st.header("Instructions")
    st.write("""
    1. Create a new Pull Request with code changes
    2. Review the differences between original and proposed code
    3. Approve or reject the PR
    4. Observe how the main branch updates after merging
    5. Complete the exercise when you understand the PR workflow
    
    This exercise simulates a real GitHub pull request workflow!
    """)