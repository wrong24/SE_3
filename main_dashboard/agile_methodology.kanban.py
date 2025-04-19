import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Kanban Board Exercise", layout="wide")
st.title("Kanban Board Exercise")

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
