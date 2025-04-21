import streamlit as st
import requests

st.set_page_config(page_title="Login - Virtual Lab", layout="centered")
st.title("Virtual Lab Login")

with st.form("login_form"):
    srn = st.text_input("SRN (Student Registration Number)", max_chars=30)
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    submit = st.form_submit_button("Login / Register")

if submit:
    if not srn or not full_name or not email:
        st.error("Please fill in all fields.")
    else:
        user_payload = {
            "username": srn,
            "full_name": full_name,
            "email": email
        }
        try:
            response = requests.post("http://integration:8026/users/", json=user_payload, timeout=3)
            if response.status_code in (200, 201):
                user = response.json()
                st.session_state["user_id"] = user["username"]
                st.success(f"Welcome, {user['full_name']}! You are now logged in.")
                st.experimental_rerun()  # Rerun to update session state
            else:
                st.error(f"Login failed: {response.text}")
        except Exception as e:
            st.error(f"Could not connect to user service: {e}")

# Redirect to main page if already logged in
if "user_id" in st.session_state:
    st.switch_page("main_dashboard/main.py")

# Optionally, show current login status
if "user_id" in st.session_state:
    st.info(f"Logged in as: {st.session_state['user_id']}")
