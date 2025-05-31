import streamlit as st
from openai import OpenAI
import os

# --- Configuration ---
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY")))

# --- Session State Setup ---
if "responses" not in st.session_state:
    st.session_state["responses"] = {}
if "step" not in st.session_state:
    st.session_state["step"] = 0
if "name" not in st.session_state:
    st.session_state["name"] = ""

# --- Page Setup ---
st.set_page_config(page_title="Orbis Onboarding", layout="centered")
st.title("🧭 Orbis Onboarding: Adaptive Learning Pathway")

st.markdown("""
Welcome! Please answer the following questions to help us personalize your learning journey.

---
Please answer honestly. Your responses will help us create a personalized onboarding experience tailored to your needs.

**Note:** Your answers are processed using secure OpenAI API services. No personal identifiers beyond your name are stored or used.
---
""")

# --- Question Function ---
def ask_question(label, key, options=None, text_input=False, question_number=None):
    if question_number:
        st.markdown(f"**Question {question_number}**")
    if text_input:
        response = st.text_input(label)
    else:
        response = st.radio(label, options)
    st.session_state["responses"][key] = response

# --- Step 0: Name ---
if st.session_state["step"] == 0:
    name = st.text_input("👋 What’s your first name?")
    if name:
        st.session_state["name"] = name
        if st.button("Start"):
            st.session_state["step"] += 1

# --- Step 1: Canvas Experience ---
elif st.session_state["step"] == 1:
    ask_question(f"{st.session_state['name']}, have you used Canvas before?", "canvas_experience", ["Yes", "No"], question_number=1)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state["step"] -= 1
    with col2:
        if st.button("Next ➡️"):
            st.session_state["step"] += 1

# --- Step 2: Advanced Canvas Review ---
elif st.session_state["step"] == 2:
    if st.session_state["responses"].get("canvas_experience") == "Yes":
        ask_question("Would you like a quick review of advanced Canvas features?", "canvas_advanced_opt_in", ["Yes", "No"], question_number=2)
    else:
        st.write("Thanks! We'll recommend a Canvas Orientation Module later.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state["step"] -= 1
    with col2:
        if st.button("Next ➡️"):
            st.session_state["step"] += 1

# --- Step 3: Writing Frequency ---
elif st.session_state["step"] == 3:
    ask_question("How often do you engage in writing?", "writing_frequency", ["Daily", "Weekly", "Occasionally", "Rarely"], question_number=3)
    if st.button("Next ➡️"):
        st.session_state["step"] += 1

# --- Step 4: Writing Type ---
elif st.session_state["step"] == 4:
    ask_question("What kinds of writing do you do most often?", "writing_type", ["Emails", "Blogs", "Academic Papers", "Social Media", "Technical Reports"], question_number=4)
    if st.button("Next ➡️"):
        st.session_state["step"] += 1

# --- Step 5: Citation Comfort ---
elif st.session_state["step"] == 5:
    ask_question("How confident are you with APA or MLA citation?", "citation_comfort", ["Very Comfortable", "Somewhat", "Not at All"], question_number=5)
    if st.button("Next ➡️"):
        st.session_state["step"] += 1

# --- Step 6: Literature Preference ---
elif st.session_state["step"] == 6:
    ask_question("What books, genres, or topics do you enjoy reading or watching?", "literature_preference", text_input=True, question_number=6)
    if st.button("Next ➡️"):
        st.session_state["step"] += 1

# --- Step 7: AI Tool Usage ---
elif st.session_state["step"] == 7:
    ask_question("Have you used tools like ChatGPT or Grammarly for school or work?", "ai_usage", ["Yes", "No"], question_number=7)
    if st.session_state["responses"].get("ai_usage") == "Yes":
        ask_question("Are you aware of the course’s AI usage policy?", "ai_policy_awareness", ["Yes", "No"], question_number=8)
    if st.button("Next ➡️"):
        st.session_state["step"] += 1

# --- Step 8: Time Management ---
elif st.session_state["step"] == 8:
    ask_question("Do you schedule weekly time to work on courses?", "time_management", ["Yes", "No", "Sometimes"], question_number=9)
    if st.button("Next ➡️"):
        st.session_state["step"] += 1

# --- Step 9: Course Intention ---
elif st.session_state["step"] == 9:
    ask_question("What do you hope to gain from this course?", "course_intention", text_input=True, question_number=10)
    if st.button("Finish and Generate My Learning Path"):
        st.session_state["step"] += 1

# --- Final Output ---
elif st.session_state["step"] == 10:
    with st.spinner("Generating your personalized onboarding plan..."):
        prompt = f"""Using the following student responses, create a 2-paragraph personalized onboarding summary for {st.session_state['name']}.
Include tone-appropriate encouragement, suggest relevant modules or tools, and embed reflection-based guidance.

Responses:
{st.session_state['responses']}

Write the summary as if you're advising a student in a warm, professional tone.
"""
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        result = response.choices[0].message.content
        st.markdown("### 🎯 Your Personalized Pathway:")
        st.write(result)
