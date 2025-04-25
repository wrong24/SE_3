import streamlit as st
import requests
from typing import Dict
import subprocess
import os
import uuid
import time
from urllib.parse import urlparse, parse_qs

def ensure_authenticated():
    # Get query parameters
    query_params = st.query_params

    # If user_id is not in session state, check URL for it
    if "user_id" not in st.session_state:
        user_id_from_url = query_params.get("user_id")  # Retrieve user_id from URL query parameters
        if user_id_from_url:
            st.session_state["user_id"] = user_id_from_url  # Store user_id in session state
            st.rerun()  # Re-run the app to reflect the updated session state
        else:
            st.warning("Please login to continue.")
            st.switch_page("pages/login.py")  # Redirect to login page if no user_id in session state

ensure_authenticated()

@st.cache_data(ttl=300) # Add this line
def verify_service(service_name: str, port: int) -> bool:
    try:
        response = requests.get(f'http://{service_name}:{port}/', timeout=2)
        print(f"Port {port} status: {response.status_code}, content: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Port {port} exception: {e}")
        return False

# Function to launch a Streamlit script in a new console
def launch_streamlit(streamlit_path: str):
    # On Windows, use "start" to launch a new cmd window running the command
    streamlit_command = f"streamlit run {streamlit_path}"
    subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", streamlit_command])

# Configure page settings
st.set_page_config(page_title="Virtual Software Engineering Lab", layout="wide")

# Define topics and their subtopics with ports and streamlit paths
TOPICS: Dict = {
    "Project Management": {
        "subtopics": {
            "SDLC": {"port": 8001, "service_name": "project_management", "streamlit_path": "project_management.sdlc.py"},
            "WBS": {"port": 8002, "service_name": "project_management", "streamlit_path": "project_management.wbs.py"},
            "Gantt Chart": {"port": 8003, "service_name": "project_management", "streamlit_path": "project_management.gantt.py"},
            "Resource Allocation": {"port": 8004, "service_name": "project_management", "streamlit_path": "project_management.resource_allocation.py"},
            "Risk Management": {"port": 8005, "service_name": "project_management", "streamlit_path": "project_management.risk_management.py"},
        },
        "description": "Learn project management fundamentals and tools"
    },
    "Collaboration Tools": {
        "subtopics": {
            "Git Flow": {"port": 8006, "service_name": "collaboration_tools", "streamlit_path": "collaboration_tools.git_flow.py"},
            "PR & Merge": {"port": 8007, "service_name": "collaboration_tools", "streamlit_path": "collaboration_tools.pr_merge.py"},
            "Chat Simulation": {"port": 8008, "service_name": "collaboration_tools", "streamlit_path": "collaboration_tools.chat_sim.py"},
            "Markdown Editor": {"port": 8009, "service_name": "collaboration_tools", "streamlit_path": "collaboration_tools.markdown_doc.py"},
            "File Share": {"port": 8010, "service_name": "collaboration_tools", "streamlit_path": "collaboration_tools.file_share.py"},
        },
        "description": "Practice with common collaboration tools and workflows"
    },
    "Agile Methodology": {
        "subtopics": {
            "Scrum Board": {"port": 8011, "service_name": "agile_methodology", "streamlit_path": "agile_methodology.scrum_board.py"},
            "Kanban": {"port": 8012, "service_name": "agile_methodology", "streamlit_path": "agile_methodology.kanban.py"},
            "User Stories": {"port": 8013, "service_name": "agile_methodology", "streamlit_path": "agile_methodology.user_stories.py"},
            "Sprint Planning": {"port": 8014, "service_name": "agile_methodology", "streamlit_path": "agile_methodology.sprint_planning.py"},
            "Burndown Chart": {"port": 8015, "service_name": "agile_methodology", "streamlit_path": "agile_methodology.burndown_chart.main.py"},
        },
        "description": "Experience Agile practices and ceremonies"
    },
    "Testing Frameworks": {
        "subtopics": {
            "Unit Testing": {"port": 8016, "service_name": "testing_frameworks", "streamlit_path": "testing_frameworks.unit_test.py"},
            "Integration Testing": {"port": 8017, "service_name": "testing_frameworks", "streamlit_path": "testing_frameworks.integration_test.py"},
            "TDD": {"port": 8018, "service_name": "testing_frameworks", "streamlit_path": "testing_frameworks.tdd_sim.py"},
            "Test Automation": {"port": 8019, "service_name": "testing_frameworks", "streamlit_path": "testing_frameworks.test_automation.py"},
            "CICD": {"port": 8020, "service_name": "testing_frameworks", "streamlit_path": "testing_frameworks.ci_cd.py"},
        },
        "description": "Learn modern testing approaches and tools"
    }
}

def get_progress():
    try:
        response = requests.get("http://integration:8024/progress/")
        return response.json() if response.status_code == 200 else {}
    except:
        return {}

def calculate_progress(topic: str, completed_items: Dict) -> float:
    topic_subtopics = set([f"{topic}_{sub}" for sub in TOPICS[topic]["subtopics"]])
    completed = topic_subtopics.intersection(set(completed_items))
    return len(completed) / len(topic_subtopics) * 100

def get_lab_attempts(user_id: str, lab_type: str):
    """
    Fetches user stats from the API server (via proxy) and finds data
    for a specific lab type.
    Assumes the API server returns a structure with 'labs_attempted'.
    """
    try:
        response = requests.get(f"http://integration:8024/progress/stats/{user_id}", timeout=10)
        response.raise_for_status()

        stats = response.json()

        # Assuming API Server returns {'labs_attempted': [{'lab_type': 'SDLC', ...}, ...]}
        labs_attempted_list = stats.get("labs_attempted", []) # Change from "breakdown"
        lab_stats_found = None
        for lab_entry in labs_attempted_list:
            if lab_entry.get("lab_type") == lab_type:
                lab_stats_found = lab_entry
                break

        return lab_stats_found if lab_stats_found else {
             "attempts": 0,
             "successful_attempts": 0,
             "success_rate": 0,
             "average_time": "N/A"
        }

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch lab attempts for user {user_id}, lab type {lab_type}: {e}")
    except Exception as e:
         print(f"An unexpected error occurred fetching lab attempts: {e}")
    return None

st.title("Virtual Software Engineering Lab")
st.write("Welcome to your interactive software engineering learning environment!")

# Get user progress
completed_items = get_progress()

# Display topics
for topic, details in TOPICS.items():
    st.header(topic)
    
    # Create two columns for progress and description
    col1, col2 = st.columns([2, 3])
    
    with col1:
        progress = calculate_progress(topic, completed_items)
        st.progress(progress / 100) # Change this line
        st.write(f"Progress: {progress:.0f}%")
    
    with col2:
        st.write(details["description"])
    
    # Create expandable section for subtopics
    with st.expander("View Subtopics"):
        for subtopic, details in details["subtopics"].items():
            completed = f"{topic}_{subtopic}" in completed_items
            status = "✅" if completed else "⬜"
            
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"{status} {subtopic}")
            with col2:
                service_status = verify_service(details["service_name"], details["port"])
                st.write("🟢" if service_status else "🔴")
            with col3:
                if st.button("Attempts", key=f"attempts_{topic}_{subtopic}"):
                    user_id = st.session_state.get("user_id", "anonymous")
                    stats_for_this_lab = get_lab_attempts(user_id, subtopic)
                    st.sidebar.empty()
                    if stats_for_this_lab and stats_for_this_lab.get("total_attempts", 0) > 0: # Check if data exists and there's at least one attempt
                        st.sidebar.title(f"{subtopic} Statistics")
                        st.sidebar.write(f"Total Attempts: {stats_for_this_lab.get('total_attempts', 'N/A')}")
                        st.sidebar.write(f"Successful Attempts: {stats_for_this_lab.get('successful_attempts', 'N/A')}")
                        success_rate = stats_for_this_lab.get('success_rate', 0)
                        st.sidebar.write(f"Success Rate: {success_rate * 100:.2f}%")
                        average_time_value = stats_for_this_lab.get('average_time', 'N/A')
                        if isinstance(average_time_value, (int, float)):
                            st.sidebar.write(f"Average Time: {average_time_value:.2f} seconds") # Format if numeric
                        else:
                            st.sidebar.write(f"Average Time: {average_time_value}") # Display as is if 'N/A' or other string
                    else:
                        st.sidebar.warning(f"No attempt data available for {subtopic}.")
            with col4:
                if st.button("Start", key=f"btn_{topic}_{subtopic}", disabled=not service_status):
                    # Track lab start event
                    try:
                        session_id = str(uuid.uuid4())

                        user_id = st.session_state.get("user_id", "anonymous") if 'st' in globals() else "anonymous"
                        start_time = time.time()

                        attempt_payload = {
                            "user_id": user_id,
                            "topic": topic,
                            "subtopic": subtopic,
                            "start_time": start_time,
                            "completion_status": False,
                            "errors_encountered": []
                        }

                        print(f"Client attempting to initiate lab attempt via proxy: POST http://integration:8024/progress/lab-attempt with payload: {attempt_payload}")

                        response = requests.post("http://integration:8024/progress/lab-attempt", json=attempt_payload)
                        
                        # Store start time in session state
                        st.session_state[f"lab_start_{subtopic}"] = start_time
                        
                        # Store lab info in session state
                        st.session_state["current_lab"] = {
                            "topic": topic,
                            "subtopic": subtopic,
                            "user_id": user_id,
                            "start_time": start_time
                        }
                        
                        # Track analytics
                        analytics_url = "http://integration:8022/analytics/event"
                        analytics_payload = {
                            "user_id": user_id,
                            "lab_type": subtopic,
                            "event_type": "start",
                            "event_data": {"session_id": session_id}
                        }
                        requests.post(analytics_url, json=analytics_payload, timeout=2)
                    except Exception as e:
                        print(f"Analytics tracking failed: {e}")
                        
                    # Launch the lab
                    if details["streamlit_path"]:
                        page_name = details['streamlit_path']
                        st.switch_page(f"pages/{page_name}")
                    else:
                        js = f"""
                        <script>
                            window.open('http://{details["service_name"]}:{details["port"]}/', '_blank');
                        </script>
                        """
                        st.components.v1.html(js, height=0)