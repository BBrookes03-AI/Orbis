import streamlit as st
import openai
import os

# --- Configuration ---
openai.api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

# --- Page Setup ---
st.set_page_config(page_title="Orbis Onboarding", layout="centered")
st.title("🧭 Orbis Onboarding: Adaptive Learning Pathway")
st.markdown("Welcome! Please answer the following questions to help us personalize your learning journey.")

# --- Session State Setup ---
if "responses" not in st.session_state:
    st.session_state["responses"] = {}

# --- Questions ---
def ask_question(label, key, options=None, text_input=False):
    if text_input:
        response = st.text_input(label)
    else:
        response = st.radio(label, options)
    st.session_state["responses"][key] = response

# Question 1: Canvas Experience
ask_question("Have you used Canvas before?", "canvas_experience", ["Yes", "No"])
if st.session_state["responses"].get("canvas_experience") == "Yes":
    ask_question("Would you like a quick review of advanced Canvas features?", "canvas_advanced_opt_in", ["Yes", "No"])

# Question 2: Writing Frequency
ask_question("How often do you engage in writing?", "writing_frequency", ["Daily", "Weekly", "Occasionally", "Rarely"])
ask_question("What kinds of writing do you do most often?", "writing_type", ["Emails", "Blogs", "Academic Papers", "Social Media", "Technical Reports"])

# Additional questions coming...

# --- Submit ---
if st.button("Generate My Learning Path"):
    with st.spinner("Generating your personalized onboarding plan..."):
        prompt = f"""Using the following responses, create a 2-paragraph personalized onboarding summary with tone, resources, and module suggestions.

Responses:
{st.session_state['responses']}

Write the summary as if you're advising a student in a warm, professional tone.
"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        result = response["choices"][0]["message"]["content"]
        st.markdown("### 🎯 Your Personalized Pathway:")
        st.write(result)
