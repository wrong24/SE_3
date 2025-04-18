import streamlit as st
import requests
import uuid
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Risk Management Exercise", layout="wide")
st.title("Risk Management")

# Risk creation form
with st.form("new_risk"):
    st.header("Add Risk")
    description = st.text_area("Risk Description")
    col1, col2 = st.columns(2)
    with col1:
        probability = st.slider("Probability (1-5)", 0.0, 1.0, 0.5, 0.1)
    with col2:
        impact = st.slider("Impact (1-5)", 1, 5, 3)
    mitigation = st.text_area("Mitigation Strategy")
    
    if st.form_submit_button("Add Risk"):
        risk = {
            "id": str(uuid.uuid4())[:8],
            "description": description,
            "probability": probability,
            "impact": impact,
            "mitigation": mitigation,
            "status": "Open"
        }
        response = requests.post("http://localhost:8005/risk", json=risk)
        if response.status_code == 200:
            st.success("Risk added!")
            st.rerun()

# Display risk matrix
response = requests.get("http://localhost:8005/risks")
if response.status_code == 200:
    risks = response.json()["risks"]
    if risks:
        st.header("Risk Matrix")
        
        # Prepare data for risk matrix
        risk_data = pd.DataFrame([
            {
                "Probability": r["probability"],
                "Impact": r["impact"],
                "Risk": f"Risk {i+1}",
                "Description": r["description"],
                "Status": r["status"]
            }
            for i, r in enumerate(risks)
        ])
        
        # Create risk matrix
        fig = px.scatter(risk_data, x="Impact", y="Probability", 
                        text="Risk", color="Status",
                        title="Risk Matrix",
                        size=[20]*len(risks))
        
        fig.update_layout(
            xaxis=dict(range=[0.5, 5.5], tick0=1, dtick=1),
            yaxis=dict(range=[0.5, 5.5], tick0=1, dtick=1)
        )
        
        st.plotly_chart(fig)
        
        # Risk management table
        st.header("Risk Register")
        for risk in risks:
            with st.expander(f"Risk: {risk['description'][:50]}..."):
                st.write(f"**Full Description:** {risk['description']}")
                st.write(f"**Probability:** {risk['probability']}")
                st.write(f"**Impact:** {risk['impact']}")
                st.write(f"**Mitigation:** {risk['mitigation']}")
                st.write(f"**Current Status:** {risk['status']}")
                
                new_status = st.selectbox(
                    "Update Status",
                    ["Open", "Mitigated", "Closed"],
                    key=f"status_{risk['id']}"
                )
                
                if new_status != risk["status"]:
                    if st.button("Update Status", key=f"update_{risk['id']}"):
                        response = requests.put(
                            f"http://localhost:8005/risk/{risk['id']}",
                            params={"status": new_status}
                        )
                        if response.status_code == 200:
                            st.success("Status updated!")
                            st.rerun()

# Complete exercise button
if len(risks) >= 3 and any(r["status"] == "Mitigated" for r in risks):
    if st.button("Complete Exercise"):
        response = requests.post("http://localhost:8005/complete_exercise")
        if response.status_code == 200:
            st.success("Exercise completed!")
            st.markdown('[Return to Dashboard](http://localhost:8000)')