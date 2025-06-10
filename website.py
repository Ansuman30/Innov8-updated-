import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os
import fitz
# ✅ Set page config as the FIRST Streamlit command
st.set_page_config(layout="wide")

# Load Data
df = pd.read_csv("mostfinaloutput.csv")
df["ID"] = df["ID"].astype(str)

# Metrics
total = len(df)
approved = len(df[df["flagged"] == 0])
fraud = len(df[df["flagged"] == 1])

st.title("Candidate Fraud Detection Dashboard")

# Page navigation
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "selected_id" not in st.session_state:
    st.session_state.selected_id = None

def display_resume_text(candidate_id):
    resume_path = os.path.join("Final_Resumes_1", f"Resume_of_ID_{candidate_id}.pdf")
    if os.path.exists(resume_path):
        with fitz.open(resume_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        st.text_area("Resume Preview", text, height=300)
    else:
        st.warning("Resume not found.")

# === Dashboard Page ===
if st.session_state.page == "Dashboard":
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Candidates", total)
    col2.metric("Approved Candidates", approved)
    col3.metric("Fraud Candidates", fraud)

    col4, col5, col6 = st.columns([2, 2, 2])

    with col4:
        st.subheader("Approved Candidates")
        for _, row in df[df["flagged"] == 0].iterrows():
            with st.container():
                st.markdown(f"**ID:** {row['ID']}  |  **Status:** Approved")
                if st.button("Resume", key=f"approved_{row['ID']}"):
                    st.session_state.selected_id = row['ID']
                    st.session_state.page = "Resume Viewer"
                    st.rerun()

    with col5:
        st.subheader("Fraud Candidates")
        for _, row in df[df["flagged"] == 1].iterrows():
            with st.container():
                st.markdown(f"**ID:** {row['ID']}  |  **Status:** Fraud")
                if st.button("Resume", key=f"fraud_{row['ID']}"):
                    st.session_state.selected_id = row['ID']
                    st.session_state.page = "Resume Viewer"
                    st.rerun()

    with col6:
        st.subheader("Candidate Distribution")
        pie_chart = px.pie(df, names=df["flagged"].map({0: "Approved", 1: "Fraud"}), hole=0.5)
        st.plotly_chart(pie_chart, use_container_width=True)

    # === Search Sidebar ===
    st.sidebar.header("Search Candidate")
    search_id = st.sidebar.text_input("Enter Candidate ID:")
    if search_id:
        candidate = df[df["ID"] == search_id]
        if not candidate.empty:
            row = candidate.iloc[0]
            st.sidebar.markdown(f"### Candidate ID: {row['ID']}")
            st.sidebar.markdown(f"- Circular Endorsement: {row.get('Number of Links', 'N/A')}")
            st.sidebar.markdown(f"- Exaggeration Score: {row.get('exaggeration_score', 'N/A')}")
            st.sidebar.markdown(f"- Number of Recommendations: {row.get('No of recommendations', 'N/A')}")
            st.sidebar.markdown(f"- Resume Score: {row.get('Score', 'N/A')}")
            st.sidebar.markdown(f"- Overall Score: {row.get('probability_score', 'N/A')}")
            st.sidebar.markdown(f"- Status: {'Approved' if row['flagged'] == 0 else 'Fraud'}")
            if st.sidebar.button("View Resume"):
                st.session_state.selected_id = row['ID']
                st.session_state.page = "Resume Viewer"
                st.rerun()
        else:
            st.sidebar.warning("ID not found.")

# === Resume Viewer Page ===
elif st.session_state.page == "Resume Viewer":
    selected_id = st.session_state.get("selected_id")
    if selected_id:
        st.title(f"Candidate ID: {selected_id}")
        candidate = df[df["ID"] == selected_id].iloc[0]
        st.markdown(f"- Circular Endorsement: {candidate.get('Number of Links', 'N/A')}")
        st.markdown(f"- Exaggeration Score: {candidate.get('exaggeration_score', 'N/A')}")
        st.markdown(f"- Number of Recommendations: {candidate.get('No of recommendations', 'N/A')}")
        st.markdown(f"- Resume Score: {candidate.get('Score', 'N/A')}")
        st.markdown(f"- Overall Score: {candidate.get('probability_score', 'N/A')}")
        st.markdown(f"- Status: {'Approved' if candidate['flagged'] == 0 else 'Fraud'}")
        display_resume_text(selected_id)
        if st.button("Go Back"):
            st.session_state.page = "Dashboard"
            st.rerun()
    else:
        st.warning("No candidate selected.")
