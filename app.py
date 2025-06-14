import streamlit as st
from openai import OpenAI
import os

# --- Configuration ---
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY")))

# --- Session State Initialization ---
if "responses" not in st.session_state:
    st.session_state["responses"] = {}
if "step" not in st.session_state:
    st.session_state["step"] = 0
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""

# --- Page Setup ---
st.set_page_config(page_title="Orbis Onboarding", layout="centered")
st.markdown("### 🧭 Orbis Onboarding: Adaptive Learning Pathway")

# --- Intro Section (Main Content) ---
st.markdown("""
Welcome! Please answer the following questions to help us personalize your learning journey.

---

Your responses will guide your onboarding experience. No scores are generated—only personalized recommendations.

---
""")

# --- Helper Function ---
def ask_question(label, key, options=None, text_input=False, question_number=None):
    if question_number is not None:
        st.markdown(
            f"""
            <div style="background-color: #ffffff; border-left: 4px solid #4F8A8B; padding: 0.75em; margin-top: 1em; margin-bottom: 1em;">
                <strong>Question {question_number}:</strong> {label}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background-color: #ffffff; border-left: 4px solid #4F8A8B; padding: 0.75em; margin-top: 1em; margin-bottom: 1em;">
                {label}
            </div>
            """,
            unsafe_allow_html=True
        )

    if text_input:
        response = st.text_input("", key=key)
    else:
        response = st.radio("", options, index=None, key=key)

    if response:
        st.session_state["responses"][key] = response
        return True
    return False


# --- Step Logic ---

# Step 0: Ask for name
if st.session_state["step"] == 0:
    ask_question("👋 What's your first name?", "name", text_input=True)
    st.session_state["user_name"] = st.session_state["responses"].get("name", "")
    col1, col2, col3 = st.columns([2, 4, 2])
    with col3:
        if st.button("Next ➡️", key="next_step0", use_container_width=True):
            st.session_state["step"] += 1

# Step 1: Canvas experience
elif st.session_state["step"] == 1:
    ask_question(
        f"{st.session_state['user_name']}, have you used Canvas before?",
        "canvas_experience",
        ["Yes", "No"],
        question_number=1,
    )
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        if st.button("⬅️ Back", key="back_step1", use_container_width=True):
            st.session_state["step"] -= 1
    with col3:
        if st.button("Next ➡️", key="next_step1", use_container_width=True):
            st.session_state["step"] += 1

# Step 2: Advanced Canvas review
elif st.session_state["step"] == 2:
    if st.session_state["responses"].get("canvas_experience") == "Yes":
        ask_question(
            "Would you like a quick review of advanced Canvas features?",
            "canvas_advanced_opt_in",
            ["Yes", "No"],
            question_number=2,
        )
    else:
        st.markdown("Thanks! We'll recommend a Canvas Orientation Module later.")
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        if st.button("⬅️ Back", key="back_step2", use_container_width=True):
            st.session_state["step"] -= 1
    with col3:
        if st.button("Next ➡️", key="next_step2", use_container_width=True):
            st.session_state["step"] += 1

# Step 3: Writing frequency
elif st.session_state["step"] == 3:
    ask_question(
        "How often do you engage in writing?",
        "writing_frequency",
        ["Daily", "Weekly", "Occasionally", "Rarely"],
        question_number=3,
    )
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        if st.button("⬅️ Back", key="back_step3", use_container_width=True):
            st.session_state["step"] -= 1
    with col3:
        if st.button("Next ➡️", key="next_step3", use_container_width=True):
            st.session_state["step"] += 1


# Step 4
elif st.session_state["step"] == 4:
    st.markdown("**Question 4**")
    st.markdown("What kinds of writing do you do most often? Select all that apply:")

    options = [
        "Emails",
        "Blogs or Newsletters",
        "Academic Papers",
        "Social Media Posts",
        "Technical Documentation",
        "Creative Writing (Poetry, Stories)",
        "Business Reports or Proposals",
        "Personal Journals or Reflections"
    ]

    # Divide into two columns
    col1, col2 = st.columns(2)
    selected = []

    for i, option in enumerate(options):
        col = col1 if i < len(options) / 2 else col2
        with col:
            if st.checkbox(option, key=f"writing_type_checkbox_{i}"):
                selected.append(option)

    # Store the combined selected options
    st.session_state["responses"]["writing_type"] = selected

    # Navigation buttons
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        if st.button("⬅️ Back", key="back_step4", use_container_width=True):
            st.session_state["step"] -= 1
    with col3:
        if st.button("Next ➡️", key="next_step4", use_container_width=True):
            st.session_state["step"] += 1


# Step 5
elif st.session_state["step"] == 5:
    ask_question(
        "How confident are you with APA or MLA citation?",
        "citation_comfort",
        ["Very Comfortable", "Somewhat", "Not at All"],
        question_number=5,
    )
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        if st.button("⬅️ Back", key="back_step1", use_container_width=True):
            st.session_state["step"] -= 1
    with col3:
        if st.button("Next ➡️", key="next_step1", use_container_width=True):
            st.session_state["step"] += 1

# Step 6
elif st.session_state["step"] == 6:
    st.markdown("**Question 6**")
    st.markdown("What books, genres, or topics do you enjoy reading or watching?")

    st.markdown(
        "<span style='font-size: 0.9em; color: gray;'>💡 Press <strong>Enter</strong> after typing your answer to continue.</span>",
        unsafe_allow_html=True
    )

    ask_question(
        label="Your answer:",
        key="literature_preference",
        text_input=True,
        question_number=None,
    )

    # Navigation buttons
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        if st.button("⬅️ Back", key="back_step6", use_container_width=True):
            st.session_state["step"] -= 1
    with col3:
        if st.button("Next ➡️", key="next_step6", use_container_width=True):
            st.session_state["step"] += 1


# Step 7
elif st.session_state["step"] == 7:
    ask_question(
        "Have you used tools like ChatGPT or Grammarly for school or work?",
        "ai_usage",
        ["Yes", "No"],
        question_number=7,
    )

    ai_used = st.session_state["responses"].get("ai_usage")

    if ai_used == "Yes":
        ask_question(
            "Are you aware of the course’s AI usage policy?",
            "ai_policy_awareness",
            ["Yes", "No"]
        )

    elif ai_used == "No":
        st.markdown(
            "<div style='background-color:#f1f1f1; padding: 0.75em; border-left: 5px solid #4CAF50;'>"
            "<strong>Note:</strong> This course will integrate AI tools to help students learn to use them ethically and effectively in the writing process."
            "</div>",
            unsafe_allow_html=True
        )

        ask_question(
            "Are you aware of the course’s AI usage policy?",
            "ai_policy_awareness",
            ["Yes", "No"]
        )

    # Navigation buttons
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        if st.button("⬅️ Back", key="back_step7", use_container_width=True):
            st.session_state["step"] -= 1
    with col3:
        if st.button("Next ➡️", key="next_step7", use_container_width=True):
            st.session_state["step"] += 1


# Step 8
elif st.session_state["step"] == 8:
    ask_question(
        "Do you schedule weekly time to work on courses?",
        "time_management",
        ["Yes", "No", "Sometimes"],
        question_number=8,
    )
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        if st.button("⬅️ Back", key="back_step1", use_container_width=True):
            st.session_state["step"] -= 1
    with col3:
        if st.button("Next ➡️", key="next_step1", use_container_width=True):
            st.session_state["step"] += 1

# Step 9
elif st.session_state["step"] == 9:
    ask_question(
        "What do you hope to gain from this course?",
        "course_intention",
        text_input=True,
        question_number=9,
    )

    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        if st.button("⬅️ Back", key="back_step9", use_container_width=True):
            st.session_state["step"] -= 1
    with col3:
        if st.button("Finish ✅", key="next_step9", use_container_width=True):
            st.session_state["step"] += 1
            st.session_state["generate_summary"] = True  # Trigger only on button press

# Step 10: Final Output
elif st.session_state["step"] == 10:
    if st.session_state.get("generate_summary", False):
        with st.spinner("Generating your personalized onboarding plan..."):
            prompt = f"""Using the following student responses, create a 2-paragraph personalized onboarding summary for {st.session_state['user_name']}.
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

        # Display GPT-generated summary
        st.markdown("### 🎯 Your Personalized Pathway:")
        st.write(result)

        # Submit to Google Sheets via Zapier
        import requests
        import datetime

        zapier_webhook_url = st.secrets.get("ZAPIER_URL")
        payload = {
            "timestamp": datetime.datetime.now().isoformat(),
            "name": st.session_state.get("user_name", ""),
            "summary": result,
            "canvas_experience": st.session_state["responses"].get("canvas_experience", ""),
            "ai_usage": st.session_state["responses"].get("ai_usage", ""),
            "ai_policy_awareness": st.session_state["responses"].get("ai_policy_awareness", "")
        }

        try:
            zapier_response = requests.post(zapier_webhook_url, json=payload)
            zapier_response.raise_for_status()
            st.success("✅ Your response has been submitted for review.")
        except Exception as e:
            st.warning("⚠️ Submission to Google Sheets failed. Please notify your instructor.")
            print("Zapier webhook error:", e)

        # Prevent re-trigger on rerun
        st.session_state["generate_summary"] = False

    # Footer
    st.markdown(
        """
        <hr style="margin-top: 2em; margin-bottom: 1em;">
        <div style='font-size: 0.8em; color: gray; text-align: center;'>
            <strong>Note:</strong> This tool uses OpenAI's API for processing your responses.
            No personal data beyond your name is stored.
        </div>
        """,
        unsafe_allow_html=True
    )
