import streamlit as st
import requests
import time
from datetime import datetime

st.set_page_config(page_title="Collaboration Platform Simulation", layout="wide")

st.title("Collaboration Platform Exercise")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'username' not in st.session_state:
    st.session_state.username = ''

# Username input
if not st.session_state.username:
    username = st.text_input("Enter your username to begin:")
    if username:
        st.session_state.username = username
        st.rerun()

if st.session_state.username:
    # Chat interface
    st.subheader(f"Welcome, {st.session_state.username}!")
    
    # Message input
    message = st.text_input("Type your message:")
    if st.button("Send"):
        if message:
            # Send message to backend
            response = requests.post(
                "http://collaboration_tools:8008/send_message",
                json={
                    "sender": st.session_state.username,
                    "content": message
                }
            )
            if response.status_code == 200:
                st.success("Message sent!")

    # Display messages
    if st.button("Refresh Messages"):
        response = requests.get("http://collaboration_tools:8008/get_messages")
        if response.status_code == 200:
            messages = response.json()
            st.session_state.messages = messages

    # Display chat history
    st.subheader("Chat History")
    for msg in st.session_state.messages:
        if isinstance(msg, dict) and "timestamp" in msg:
            timestamp = datetime.fromtimestamp(msg['timestamp']).strftime('%H:%M:%S')
            st.write(f"[{timestamp}] {msg['sender']}: {msg['content']}")
        else:
            # Fallback for non-dict messages
            st.write(msg)

    # Complete exercise button
    if st.button("Complete Exercise"):
        response = requests.post("http://collaboration_tools:8008/complete_exercise")
        if response.status_code == 200:
            st.success("Exercise completed! You can now move to the next topic.")
            st.markdown('[Return to Dashboard](http://main_services:8000)')

# Instructions sidebar
with st.sidebar:
    st.header("Instructions")
    st.write("""
    1. Enter your username to begin
    2. Send at least 5 messages
    3. Try refreshing to see message updates
    4. Click 'Complete Exercise' when done
    """)