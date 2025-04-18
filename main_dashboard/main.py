import streamlit as st
import requests
from typing import Dict
import subprocess

# Add after imports
def verify_service(port: int) -> bool:
    try:
        # Get service name based on port
        service_name = get_service_name(port)
        response = requests.get(f'http://{service_name}/', timeout=2)
        return response.status_code == 200
    except:
        return False

def get_service_name(port: int) -> str:
    # Map ports to service names defined in docker-compose
    port_to_service = {
        8001: "sdlc_service",
        8002: "wbs_service",
        8003: "gantt_service",
        8004: "resource_service",
        8005: "risk_service",
        8006: "git_service",
        8007: "pr_service",
        8008: "chat_service",
        8009: "markdown_service",
        8010: "fileshare_service",
        8011: "scrum_service",
        8012: "kanban_service",
        8013: "stories_service",
        8014: "sprint_service",
        8015: "burndown_service",
        8016: "unit_test_service",
        8017: "integration_test_service",
        8018: "tdd_service",
        8019: "automation_service",
        8020: "cicd_service"
    }
    return port_to_service.get(port, "unknown_service")

# Function to launch a Streamlit script in a new console
def launch_streamlit(command: str):
    # On Windows, use "start" to launch a new cmd window running the command
    subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", command])

# Configure page settings
st.set_page_config(page_title="Virtual Software Engineering Lab", layout="wide")

# Define topics and their subtopics with ports
TOPICS: Dict = {
    "Project Management": {
        "subtopics": ["SDLC", "WBS", "Gantt Chart", "Resource Allocation", "Risk Management"],
        "ports": range(8001, 8006),
        "description": "Learn project management fundamentals and tools"
    },
    "Collaboration Tools": {
        "subtopics": ["Git Flow", "PR & Merge", "Chat Simulation", "Markdown Editor", "File Share"],
        "ports": range(8006, 8011),
        "description": "Practice with common collaboration tools and workflows"
    },
    "Agile Methodology": {
        "subtopics": ["Scrum Board", "Kanban", "User Stories", "Sprint Planning", "Burndown Chart"],
        "ports": range(8011, 8016),
        "description": "Experience Agile practices and ceremonies"
    },
    "Testing Frameworks": {
        "subtopics": ["Unit Testing", "Integration Testing", "TDD", "Test Automation", "CI/CD"],
        "ports": range(8016, 8021),
        "description": "Learn modern testing approaches and tools"
    }
}

def get_progress():
    try:
        response = requests.get("http://progress_service:9000/progress")
        return response.json() if response.status_code == 200 else {}
    except:
        return {}

def calculate_progress(topic: str, completed_items: Dict) -> float:
    topic_subtopics = set([f"{topic}_{sub}" for sub in TOPICS[topic]["subtopics"]])
    completed = topic_subtopics.intersection(set(completed_items))
    return len(completed) / len(topic_subtopics) * 100

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
        st.progress(progress)
        st.write(f"Progress: {progress:.0f}%")
    
    with col2:
        st.write(details["description"])
    
    # Create expandable section for subtopics
    with st.expander("View Subtopics"):
        for subtopic, port in zip(details["subtopics"], details["ports"]):
            completed = f"{topic}_{subtopic}" in completed_items
            status = "✅" if completed else "⬜"
            
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"{status} {subtopic}")
            with col2:
                service_status = verify_service(port)
                st.write("🟢" if service_status else "🔴")
            with col3:
                if st.button("Start", key=f"btn_{topic}_{subtopic}", disabled=not service_status):
                    if topic == "Project Management" and subtopic == "SDLC":
                        launch_streamlit("streamlit run project_management/sdlc/main.py")
                    else:
                        service_name = get_service_name(port)
                        js = f"""
                        <script>
                            window.open('http://{service_name}/', '_blank');
                        </script>
                        """
                        st.components.v1.html(js, height=0)