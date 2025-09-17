# app.py
import streamlit as st
from analyzer import analyze_candidate
from utils import extract_text_from_pdf


st.set_page_config(page_title="AI Intern Hiring System", layout="wide")

# Storage for candidate analyses
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = []

st.title("🤖 AI-Powered Intern Hiring System")
st.write(
    "Upload a candidate’s **resume** and **transcript** to analyze their "
    "strengths, growth areas, usefulness, job fit score, project ideas, and interview questions."
)

resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
transcript_file = st.file_uploader("Upload Transcript (PDF)", type="pdf")


def display_analysis(result: dict, candidate_name="Candidate"):
    st.subheader(f"📊 {candidate_name} Analysis")

    # Job Fit Score
    st.metric("🎯 Job Fit Score", f"{result.get('job_fit_score', 0)}%")

    # Strengths & Growth Areas
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✅ Strengths")
        for s in result.get("strengths", []):
            st.markdown(f"- {s}")
    with col2:
        st.markdown("### 🌱 Growth Areas")
        for g in result.get("growth_areas", []):
            st.markdown(f"- {g}")

    # Usefulness
    st.markdown("### 💡 Usefulness")
    for u in result.get("usefulness", []):
        st.markdown(f"- {u}")

    # AI Project Suggestions
    st.markdown("### 📂 Suggested AI Projects")
    for p in result.get("ai_projects", []):
        st.markdown(f"- {p}")

    # Interview Questions (always show instead of button)
    st.markdown("### 📋 Interview Questions")
    for q in result.get("interview_questions", []):
        st.markdown(f"- {q}")

    # Summary
    st.markdown("### 📝 Summary")
    st.write(result.get("summary", ""))

    return result


if resume_file and transcript_file:
    if st.button("Analyze Candidate"):
        with st.spinner("Analyzing with Gemini..."):
            resume_text = extract_text_from_pdf(resume_file)
            transcript_text = extract_text_from_pdf(transcript_file)
            result = analyze_candidate(resume_text, transcript_text)

        candidate_data = display_analysis(result)
        if candidate_data:
            st.session_state.candidate_data.append(candidate_data)
