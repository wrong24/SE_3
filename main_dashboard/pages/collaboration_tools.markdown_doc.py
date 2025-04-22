import streamlit as st
import requests
from streamlit.components.v1 import html

st.set_page_config(page_title="Markdown Documentation Exercise", layout="wide")

st.title("Markdown Documentation Exercise")

# Initialize session state
if 'current_doc' not in st.session_state:
    st.session_state.current_doc = ""
if 'preview_mode' not in st.session_state:
    st.session_state.preview_mode = False

# Document title input
doc_title = st.text_input("Document Title", key="doc_title")

# Create two columns for editor and preview
col1, col2 = st.columns(2)

with col1:
    st.subheader("Markdown Editor")
    markdown_content = st.text_area("", height=400, key="markdown_content")
    
    if st.button("Save Document"):
        if doc_title and markdown_content:
            response = requests.post(
                "http://collaboration_tools:8009/save",
                json={"title": doc_title, "content": markdown_content}
            )
            if response.status_code == 200:
                st.success("Document saved successfully!")
                st.session_state.current_doc = doc_title

with col2:
    st.subheader("Preview")
    if markdown_content:
        st.markdown(markdown_content)

# Document list
st.sidebar.header("Saved Documents")
response = requests.get("http://collaboration_tools:8009/list")
if response.status_code == 200:
    documents = response.json()["documents"]
    for doc in documents:
        if st.sidebar.button(doc):
            response = requests.get(f"http://collaboration_tools:8009/document/{doc}")
            if response.status_code == 200:
                st.session_state.doc_title = doc
                st.session_state.markdown_content = response.json()["content"]
                st.experimental_rerun()

# Markdown reference guide
with st.sidebar:
    st.header("Markdown Guide")
    st.markdown("""
    ### Basic Syntax
    - `# Heading 1`
    - `## Heading 2`
    - `**bold**`
    - `*italic*`
    - `- bullet point`
    - `1. numbered list`
    - `[link](url)`
    - ````code block````
    """)

# Complete exercise button
if st.button("Complete Exercise"):
    response = requests.post("http://collaboration_tools:8009/complete_exercise")
    if response.status_code == 200:
        st.success("Exercise completed! You can now move to the next topic.")
        st.markdown('[Return to Dashboard](http://main_services:8000)')

if st.button("Return to Dashboard"):
    st.markdown("<meta http-equiv='refresh' content='0; url=http://localhost:8000'>", unsafe_allow_html=True)

# Exercise instructions
with st.sidebar:
    st.header("Instructions")
    st.write("""
    1. Create a new document with a title
    2. Write markdown content using the editor
    3. Preview your changes in real-time
    4. Save your document
    5. Try loading and editing existing documents
    6. Complete the exercise when you're comfortable with markdown
    """)