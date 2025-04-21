import streamlit as st
import requests

st.set_page_config(page_title="Unit Testing Exercise", layout="wide")
st.title("Unit Testing with PyTest")

# Default code templates
default_function = '''def calculate_sum(a: int, b: int) -> int:
    return a + b

def is_palindrome(text: str) -> bool:
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]'''

default_test = '''def test_calculate_sum():
    assert calculate_sum(2, 3) == 5
    assert calculate_sum(-1, 1) == 0

def test_palindrome():
    assert is_palindrome("A man a plan a canal Panama")
    assert not is_palindrome("hello")'''

col1, col2 = st.columns(2)

with col1:
    st.subheader("Function Implementation")
    function_code = st.text_area("Write your functions here:", 
                                value=default_function, height=300)

with col2:
    st.subheader("Test Cases")
    test_code = st.text_area("Write your tests here:", 
                            value=default_test, height=300)

if st.button("Run Tests"):
    response = requests.post(
        "http://testing_frameworks:8016/run_test",
        json={
            "function_code": function_code,
            "test_code": test_code
        }
    )
    if response.status_code == 200:
        result = response.json()
        st.code(result["output"], language="text")
        if "FAILED" not in result["output"]:
            st.success("All tests passed!")
        else:
            st.error("Some tests failed!")

# Instructions
with st.sidebar:
    st.header("Instructions")
    st.markdown("""
    1. Write your function implementation in the left panel
    2. Write corresponding test cases in the right panel
    3. Click 'Run Tests' to execute
    4. Ensure all tests pass to complete the exercise
    
    **Testing Tips:**
    - Use `assert` statements to verify expectations
    - Test both valid and edge cases
    - Write clear, focused test functions
    """)

# Exercise completion criteria
if st.button("Complete Exercise"):
    response = requests.post("http://testing_frameworks:8016/complete_exercise")
    if response.status_code == 200:
        st.success("Exercise completed!")
        st.markdown('[Return to Dashboard](http://main_services:8000)')