import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os
import zipfile

# === Auto-extract ZIPs if present ===
def extract_zip_once(zip_path, extract_to):
    if os.path.exists(zip_path) and not os.path.exists(extract_to):
        os.makedirs(extract_to, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        st.info(f"Extracted {os.path.basename(zip_path)} to {extract_to}")

# Paths to your ZIP files and target folders
resume_zip_path = "Final_Resumes.zip"
rec_zip_path = "Final_Recommendations.zip"
resume_extract_path = "Final_Resumes_1"
rec_extract_path = "Final_Recommendations_1"

extract_zip_once(resume_zip_path, resume_extract_path)
extract_zip_once(rec_zip_path, rec_extract_path)

# Load Data
df = pd.read_csv("mostfinaloutput.csv")
df["ID"] = df["ID"].astype(str)

# Metrics
total = len(df)
approved = len(df[df["flagged"] == 0])
fraud = len(df[df["flagged"] == 1])

# Streamlit UI setup
st.set_page_config(layout="wide")
st.title("Candidate Fraud Detection Dashboard")

# Page navigation
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "selected_id" not in st.session_state:
    st.session_state.selected_id = None

# Shared resume display function
def display_resume(candidate_id):
    resume_path = os.path.join("Final_Resumes", f"Resume_of_ID_{candidate_id}.pdf")
    if os.path.exists(resume_path):
        with open(resume_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="Resume_of_ID_{candidate_id}.pdf">Click to download Resume</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("Resume not found.")

if st.session_state.page == "Dashboard":
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Candidates", total)
    col2.metric("Approved Candidates", approved)
    col3.metric("Fraud Candidates", fraud)

    col4, col5, col6 = st.columns([2, 2, 2])

    # Approved Candidates
    with col4:
        st.subheader("Approved Candidates")
        for _, row in df[df["flagged"] == 0].iterrows():
            with st.container():
                st.markdown(f"**ID:** {row['ID']}  |  **Status:** Approved")
                if st.button("Resume", key=f"approved_{row['ID']}"):
                    st.session_state.selected_id = row['ID']
                    st.session_state.page = "Resume Viewer"
                    st.rerun()

    # Fraud Candidates
    with col5:
        st.subheader("Fraud Candidates")
        for _, row in df[df["flagged"] == 1].iterrows():
            with st.container():
                st.markdown(f"**ID:** {row['ID']}  |  **Status:** Fraud")
                if st.button("Resume", key=f"fraud_{row['ID']}"):
                    st.session_state.selected_id = row['ID']
                    st.session_state.page = "Resume Viewer"
                    st.rerun()

    # Pie Chart
    with col6:
        st.subheader("Candidate Distribution")
        pie_chart = px.pie(df, names=df["flagged"].map({0: "Approved", 1: "Fraud"}), hole=0.5)
        st.plotly_chart(pie_chart, use_container_width=True)

    # Search Functionality
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
        display_resume(selected_id)
        if st.button("Go Back"):
            st.session_state.page = "Dashboard"
            st.rerun()
    else:
        st.warning("No candidate selected.")


import zipfile
import tempfile
from pathlib import Path




resume_extract_path = "Final_Resumes"
rec_extract_path = "Final_Recommendations"




