import streamlit as st
import google.generativeai as ai
import json
import re

# Configure Gemini
API_KEY = "AIzaSyAwv9u_ln4BFXRjqs1Y_1GBXcWcKZXYnC0"
ai.configure(api_key=API_KEY)

model = ai.GenerativeModel("gemini-2.0-flash-exp")

def analyze_candidate(resume_text, transcript_text):
    prompt = f"""
    You are an AI assistant helping to evaluate interns for an AI Education Hub.

    Job Scope:
    1. Assist/lead AI workshops
    2. Come up with AI workshop ideas
    3. Do a project related to their course, but integrated with AI
    4. Perform ad-hoc tasks at the AI Education Hub

    Candidate Resume:
    {resume_text}

    Candidate Transcript:
    {transcript_text}

    Return ONLY a valid JSON object with the following fields:
    {{
      "strengths": [ "list of strengths" ],
      "growth_areas": [ "list of growth areas" ],
      "usefulness": [ "how they can contribute" ],
      "ai_projects": [ "possible AI project ideas" ],
      "interview_questions": [ "interview questions" ],
      "job_fit_score": 0-100,
      "summary": "short paragraph summary"
    }}
    """

    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    # Remove markdown fences if present
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```[a-zA-Z0-9]*\n", "", raw_text)  # remove opening ```
        raw_text = re.sub(r"\n```$", "", raw_text)              # remove closing ```

    # Try JSON parsing
    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        # fallback: wrap into dict so app still runs
        result = {
            "strengths": [],
            "growth_areas": [],
            "usefulness": [],
            "ai_projects": [],
            "interview_questions": [],
            "job_fit_score": 0,
            "summary": f"⚠️ Parsing failed. Raw output: {raw_text}"
        }

    return result
