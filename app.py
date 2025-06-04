(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app.py b/app.py
index b6f180e7e31b519a01ab714762e75f6cdb69b767..8dfb2c358b7a51bb0ff26ef4491ca0aecbfa2482 100644
--- a/app.py
+++ b/app.py
@@ -1,150 +1,205 @@
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
-if "name" not in st.session_state:
-    st.session_state["name"] = ""
+if "user_name" not in st.session_state:
+    st.session_state["user_name"] = ""
 
 # --- Page Setup ---
 st.set_page_config(page_title="Orbis Onboarding", layout="centered")
 st.markdown("### 🧭 Orbis Onboarding: Adaptive Learning Pathway")
 
 st.markdown("""
 Welcome! Please answer the following questions to help us personalize your learning journey.
 
 ---
 Your responses will guide your onboarding experience. No scores are generated—only personalized recommendations.
 
 **Note:** This tool uses OpenAI's API for processing your responses. No personal data beyond your name is stored.
 ---
 """)
 
 # --- Helper Function ---
 def ask_question(label, key, options=None, text_input=False, question_number=None):
     if question_number is not None:
         st.markdown(f"**Question {question_number}**")
     if text_input:
-        response = st.text_input(label)
+        response = st.text_input(label, key=key)
     else:
-        response = st.radio(label, options)
+        response = st.radio(label, options, index=None, key=key)
     if response:
         st.session_state["responses"][key] = response
         return True
     return False
 
 # --- Step Logic ---
 
 # Step 0: Name
 if st.session_state["step"] == 0:
-    if ask_question("👋 What's your first name?", "name", text_input=True):
-        st.session_state["name"] = st.session_state["responses"]["name"]
-    if st.button("Start ➡️"):
+    ask_question("👋 What's your first name?", "name", text_input=True)
+    st.session_state["user_name"] = st.session_state["responses"].get("name", "")
+    if st.button("Start ➡️", key="next_step0"):
         st.session_state["step"] += 1
 
 # Step 1
 elif st.session_state["step"] == 1:
-    if ask_question(f"{st.session_state['name']}, have you used Canvas before?", "canvas_experience", ["Yes", "No"], question_number=1):
-        if st.button("Next ➡️"):
-            st.session_state["step"] += 1
-    if st.button("⬅️ Back"):
+    ask_question(
+        f"{st.session_state['user_name']}, have you used Canvas before?",
+        "canvas_experience",
+        ["Yes", "No"],
+        question_number=1,
+    )
+    if st.button("Next ➡️", key="next_step1"):
+        st.session_state["step"] += 1
+    if st.button("⬅️ Back", key="back_step1"):
         st.session_state["step"] -= 1
 
 # Step 2
 elif st.session_state["step"] == 2:
     if st.session_state["responses"].get("canvas_experience") == "Yes":
-        ask_question("Would you like a quick review of advanced Canvas features?", "canvas_advanced_opt_in", ["Yes", "No"], question_number=2)
+        ask_question(
+            "Would you like a quick review of advanced Canvas features?",
+            "canvas_advanced_opt_in",
+            ["Yes", "No"],
+            question_number=2,
+        )
     else:
         st.markdown("Thanks! We'll recommend a Canvas Orientation Module later.")
-    if st.button("Next ➡️"):
+    if st.button("Next ➡️", key="next_step2"):
         st.session_state["step"] += 1
-    if st.button("⬅️ Back"):
+    if st.button("⬅️ Back", key="back_step2"):
         st.session_state["step"] -= 1
 
 # Step 3
 elif st.session_state["step"] == 3:
-    if ask_question("How often do you engage in writing?", "writing_frequency", ["Daily", "Weekly", "Occasionally", "Rarely"], question_number=3):
-        if st.button("Next ➡️"):
-            st.session_state["step"] += 1
-    if st.button("⬅️ Back"):
+    ask_question(
+        "How often do you engage in writing?",
+        "writing_frequency",
+        ["Daily", "Weekly", "Occasionally", "Rarely"],
+        question_number=3,
+    )
+    if st.button("Next ➡️", key="next_step3"):
+        st.session_state["step"] += 1
+    if st.button("⬅️ Back", key="back_step3"):
         st.session_state["step"] -= 1
 
 # Step 4
 elif st.session_state["step"] == 4:
-    if ask_question("What kinds of writing do you do most often?", "writing_type", ["Emails", "Blogs", "Academic Papers", "Social Media", "Technical Reports"], question_number=4):
-        if st.button("Next ➡️"):
-            st.session_state["step"] += 1
-    if st.button("⬅️ Back"):
+    ask_question(
+        "What kinds of writing do you do most often?",
+        "writing_type",
+        [
+            "Emails",
+            "Blogs",
+            "Academic Papers",
+            "Social Media",
+            "Technical Reports",
+        ],
+        question_number=4,
+    )
+    if st.button("Next ➡️", key="next_step4"):
+        st.session_state["step"] += 1
+    if st.button("⬅️ Back", key="back_step4"):
         st.session_state["step"] -= 1
 
 # Step 5
 elif st.session_state["step"] == 5:
-    if ask_question("How confident are you with APA or MLA citation?", "citation_comfort", ["Very Comfortable", "Somewhat", "Not at All"], question_number=5):
-        if st.button("Next ➡️"):
-            st.session_state["step"] += 1
-    if st.button("⬅️ Back"):
+    ask_question(
+        "How confident are you with APA or MLA citation?",
+        "citation_comfort",
+        ["Very Comfortable", "Somewhat", "Not at All"],
+        question_number=5,
+    )
+    if st.button("Next ➡️", key="next_step5"):
+        st.session_state["step"] += 1
+    if st.button("⬅️ Back", key="back_step5"):
         st.session_state["step"] -= 1
 
 # Step 6
 elif st.session_state["step"] == 6:
-    if ask_question("What books, genres, or topics do you enjoy reading or watching?", "literature_preference", text_input=True, question_number=6):
-        if st.button("Next ➡️"):
-            st.session_state["step"] += 1
-    if st.button("⬅️ Back"):
+    ask_question(
+        "What books, genres, or topics do you enjoy reading or watching?",
+        "literature_preference",
+        text_input=True,
+        question_number=6,
+    )
+    if st.button("Next ➡️", key="next_step6"):
+        st.session_state["step"] += 1
+    if st.button("⬅️ Back", key="back_step6"):
         st.session_state["step"] -= 1
 
 # Step 7
 elif st.session_state["step"] == 7:
-    if ask_question("Have you used tools like ChatGPT or Grammarly for school or work?", "ai_usage", ["Yes", "No"], question_number=7):
-        if st.session_state["responses"]["ai_usage"] == "Yes":
-            ask_question("Are you aware of the course’s AI usage policy?", "ai_policy_awareness", ["Yes", "No"])
-        if st.button("Next ➡️"):
-            st.session_state["step"] += 1
-    if st.button("⬅️ Back"):
+    ask_question(
+        "Have you used tools like ChatGPT or Grammarly for school or work?",
+        "ai_usage",
+        ["Yes", "No"],
+        question_number=7,
+    )
+    if st.session_state["responses"].get("ai_usage") == "Yes":
+        ask_question(
+            "Are you aware of the course’s AI usage policy?",
+            "ai_policy_awareness",
+            ["Yes", "No"],
+        )
+    if st.button("Next ➡️", key="next_step7"):
+        st.session_state["step"] += 1
+    if st.button("⬅️ Back", key="back_step7"):
         st.session_state["step"] -= 1
 
 # Step 8
 elif st.session_state["step"] == 8:
-    if ask_question("Do you schedule weekly time to work on courses?", "time_management", ["Yes", "No", "Sometimes"], question_number=8):
-        if st.button("Next ➡️"):
-            st.session_state["step"] += 1
-    if st.button("⬅️ Back"):
+    ask_question(
+        "Do you schedule weekly time to work on courses?",
+        "time_management",
+        ["Yes", "No", "Sometimes"],
+        question_number=8,
+    )
+    if st.button("Next ➡️", key="next_step8"):
+        st.session_state["step"] += 1
+    if st.button("⬅️ Back", key="back_step8"):
         st.session_state["step"] -= 1
 
 # Step 9
 elif st.session_state["step"] == 9:
-    if ask_question("What do you hope to gain from this course?", "course_intention", text_input=True, question_number=9):
-        if st.button("Finish and Generate My Learning Path"):
-            st.session_state["step"] += 1
-    if st.button("⬅️ Back"):
+    ask_question(
+        "What do you hope to gain from this course?",
+        "course_intention",
+        text_input=True,
+        question_number=9,
+    )
+    if st.button("Finish and Generate My Learning Path", key="next_step9"):
+        st.session_state["step"] += 1
+    if st.button("⬅️ Back", key="back_step9"):
         st.session_state["step"] -= 1
 
 # Step 10: Final Output
 elif st.session_state["step"] == 10:
     with st.spinner("Generating your personalized onboarding plan..."):
-        prompt = f"""Using the following student responses, create a 2-paragraph personalized onboarding summary for {st.session_state['name']}.
+        prompt = f"""Using the following student responses, create a 2-paragraph personalized onboarding summary for {st.session_state['user_name']}.
 Include tone-appropriate encouragement, suggest relevant modules or tools, and embed reflection-based guidance.
 
 Responses:
 {st.session_state['responses']}
 
 Write the summary as if you're advising a student in a warm, professional tone.
 """
         response = client.chat.completions.create(
             model="gpt-4",
             messages=[
                 {"role": "user", "content": prompt}
             ],
             temperature=0.7,
             max_tokens=500
         )
         result = response.choices[0].message.content
         st.markdown("### 🎯 Your Personalized Pathway:")
         st.write(result)
 
EOF
)
