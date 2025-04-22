import streamlit as st
import requests
import os
from io import BytesIO

st.set_page_config(page_title="File Sharing Exercise", layout="wide")

st.title("Distributed File Transfer Exercise")

# File upload section
st.header("Upload Files")
uploaded_file = st.file_uploader("Choose a file to share", type=["txt", "pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    if st.button("Upload"):
        files = {"file": uploaded_file}
        response = requests.post("http://collaboration_tools:8010/upload", files=files)
        if response.status_code == 200:
            st.success(f"File {uploaded_file.name} uploaded successfully!")
        else:
            st.error("Upload failed!")

# File listing and download section
st.header("Shared Files")
if st.button("Refresh File List"):
    response = requests.get("http://collaboration_tools:8010/files")
    if response.status_code == 200:
        files = response.json()["files"]
        if not files:
            st.info("No files have been shared yet.")
        else:
            for file in files:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(file)
                with col2:
                    if st.button("Download", key=file):
                        response = requests.get(f"http://collaboration_tools:8010/download/{file}")
                        if response.status_code == 200:
                            st.download_button(
                                label="Save File",
                                data=BytesIO(response.content),
                                file_name=file,
                                mime="application/octet-stream",
                                key=f"download_{file}"
                            )

# Complete exercise button
if st.button("Complete Exercise"):
    response = requests.post("http://collaboration_tools:8010/complete_exercise")
    if response.status_code == 200:
        st.success("Exercise completed! You can now move to the next topic.")
        st.markdown('[Return to Dashboard](http://main_services:8000)')

if st.button("Return to Dashboard"):
    st.markdown("<meta http-equiv='refresh' content='0; url=http://localhost:8000'>", unsafe_allow_html=True)

# Instructions sidebar
with st.sidebar:
    st.header("Instructions")
    st.write("""
    1. Upload at least one file to share
    2. View the list of shared files
    3. Download a shared file
    4. Complete the exercise when you're done
    
    This exercise simulates a basic file sharing system similar to those used in collaborative development environments.
    """)