import streamlit as st
import requests
from typing import Dict
import subprocess
import os

# Add after imports
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
        for subtopic, details in details["subtopics"].items():
            completed = f"{topic}_{subtopic}" in completed_items
            status = "✅" if completed else "⬜"
            
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"{status} {subtopic}")
            with col2:
                service_status = verify_service(details["service_name"], details["port"])
                st.write("🟢" if service_status else "🔴")
            with col3:
                if st.button("Start", key=f"btn_{topic}_{subtopic}", disabled=not service_status):
                    if details["streamlit_path"]:
                        # Always launch on port 8501
                        streamlit_app_path = details["streamlit_path"]
                        # Kill any process using port 8501 before starting a new one
                        import psutil
                        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                            try:
                                if 'streamlit' in proc.info['name'].lower() or \
                                   (proc.info['cmdline'] and any('streamlit' in arg for arg in proc.info['cmdline'])):
                                    if proc.info['cmdline'] and any('--server.port=8501' in arg for arg in proc.info['cmdline']):
                                        proc.kill()
                            except Exception:
                                pass
                        subprocess.Popen(["streamlit", "run", streamlit_app_path, "--server.port=8501"])
                    else:
                        js = f"""
                        <script>
                            window.open('http://{details["service_name"]}:{details["port"]}/', '_blank');
                        </script>
                        """
                        st.components.v1.html(js, height=0)