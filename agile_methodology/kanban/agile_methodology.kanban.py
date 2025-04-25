import streamlit as st
import requests
import uuid
import urllib.parse

st.set_page_config(page_title="Kanban Board Exercise", layout="wide")
st.title("Kanban Board Exercise")

# Restore session state from query params if present
query_params = st.query_params
if 'user_id' in query_params and 'start_time' in query_params:
    st.session_state['current_lab'] = {
        'user_id': query_params['user_id'][0],
        'start_time': query_params['start_time'][0]
    }

# Create new card form
with st.form("new_card"):
    st.header("Create New Card")
    title = st.text_input("Card Title")
    description = st.text_area("Description")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    
    if st.form_submit_button("Create Card"):
        card = {
            "id": str(uuid.uuid4())[:8],
            "title": title,
            "description": description,
            "priority": priority,
            "status": "backlog"
        }
        response = requests.post("http://agile_methodology:8012/card", json=card)
        if response.status_code == 200:
            st.success("Card created!")

# Display board
st.header("Kanban Board")
response = requests.get("http://agile_methodology:8012/board")
if response.status_code == 200:
    board = response.json()
    
    cols = st.columns(5)
    for i, (status, cards) in enumerate(board.items()):
        with cols[i]:
            st.subheader(status.upper())
            for card in cards:
                with st.container():
                    st.markdown(f"**{card['title']}**")
                    st.markdown(f"Priority: {card['priority']}")
                    st.write(card['description'])
                    new_status = st.selectbox(
                        "Move to",
                        ["backlog", "ready", "development", "testing", "done"],
                        key=f"move_{card['id']}"
                    )
                    if new_status != card['status']:
                        requests.put(
                            f"http://agile_methodology:8012/card/{card['id']}",
                            params={"new_status": new_status}
                        )
                        st.experimental_rerun()
                    st.markdown("---")

# Complete exercise button and instructions
st.sidebar.header("Instructions")
st.sidebar.write("""
1. Create new cards with priorities
2. Move cards through different stages
3. Observe WIP limits
4. Practice Kanban flow
""")

if st.button("Complete Exercise"):
    response = requests.post("http://agile_methodology:8012/complete_exercise")
    if response.status_code == 200:
        st.success("Exercise completed!")
        st.markdown('[Return to Dashboard](http://main_services:8000)')

if st.button("Return to Dashboard"):
    # Preserve session parameters when returning to dashboard
    current_lab = st.session_state.get("current_lab", {})
    user_id = current_lab.get("user_id", "")
    start_time = current_lab.get("start_time", "")
    params = urllib.parse.urlencode({"user_id": user_id, "start_time": start_time})
    st.switch_page(f"main.py?{params}")
