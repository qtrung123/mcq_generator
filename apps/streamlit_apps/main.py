import streamlit as st
import json
import sys
from pathlib import Path
import litellm
import logging

st.set_page_config(page_title="MCQ Generator", layout="wide")
# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from mcq_generator.mcq_generator import QuestionGenerator
from mcq_generator.question_prerequsite import QuestionPrerequisite
from mcq_generator.similar_question_generator import SimilarQuestionGenerator
from mcq_generator.prompt_builder import PromptBuilder

# Initialize logging
logging.basicConfig(level=logging.INFO, filename='mcqapp.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

# Function to save questions to a JSON file
def save_to_json_in_english(filename, questions):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

# Main Streamlit Application
def main():
    st.sidebar.title("MCQ Generator")

    # Model selection
    model = st.sidebar.selectbox(
        "Select Model",
        [
            "gemini/gemini-2.5-flash-lite",
            "gemini/gemini-2.5-flash",
            "openai/gpt-4o-mini"
        ]
    )
    language = "English"
    
    # User inputs
    specialization = st.sidebar.text_input("Enter the specialization:")
    difficulty = st.sidebar.selectbox("Select difficulty level:", ["Easy", "Medium", "Hard"])
    num_questions = st.sidebar.number_input("Number of questions:", min_value=1, max_value=100, value=5)
    with st.sidebar.expander("Advanced Settings"):
        max_tokens_question = st.number_input(
            "Max Tokens for Question Generation",
            min_value=100,
            max_value=4000,
            value=3000
        )

        max_tokens_explanation = st.number_input(
            "Max Tokens for Explanation",
            min_value=100,
            max_value=4000,
            value=1500
    )

    # Initialize session state
    if "original_questions" not in st.session_state:
        st.session_state.original_questions = {}
    if "last_index" not in st.session_state:
        st.session_state.last_index = {}
    
    if "answer_feedback" not in st.session_state:
        st.session_state.answer_feedback = {}

    if "explanation_result" not in st.session_state:
        st.session_state.explanation_result = {}

    if "prerequisite_result" not in st.session_state:
        st.session_state.prerequisite_result = {}

    if "similar_result" not in st.session_state:
        st.session_state.similar_result = {}

    # Generate Questions
    if st.sidebar.button("Generate Questions"):
        if not model:
            st.sidebar.error("Please select a valid model.")
        elif not specialization or not difficulty:
            st.sidebar.error("Please fill out all fields.")
        else:
            # Clear previous UI results
            st.session_state.answer_feedback = {}
            st.session_state.explanation_result = {}
            st.session_state.prerequisite_result = {}
            st.session_state.similar_result = {}

            # Clear previous generated questions before creating a new demo set
            st.session_state.original_questions = {}
            st.session_state.last_index = {}

            specialization = specialization.strip()
            st.session_state.original_questions[specialization] = {}
            st.session_state.last_index[specialization] = 0

            with st.spinner("Generating questions..."):
                question_generator = QuestionGenerator(model)
                questions = question_generator.generate_questions(specialization, difficulty, num_questions, max_tokens_question, 4)
                for index, q in enumerate(questions, start=1):
                    question_text = q.get("question", "")
                    options = q.get("options", {})
                    correct_answer = q.get("correct_answer", "")

                    # Convert options list to dictionary if needed
                    if isinstance(options, list):
                        options = {
                            chr(65 + idx): option
                            for idx, option in enumerate(options)
                        }

                    # Normalize correct answer
                    if isinstance(correct_answer, list):
                        correct_answer = correct_answer[0] if correct_answer else ""

                    correct_answer = str(correct_answer).strip().upper()

                    # Keep only the first letter if model returns "C. answer text"
                    if correct_answer:
                        correct_answer = correct_answer[0]

                    if question_text and options:
                        question_id = f"{specialization}_{index}"

                        st.session_state.original_questions[specialization][question_id] = {
                            "question": question_text,
                            "options": options,
                            "correct_answer": correct_answer,
                            "translations": {}
                        }
                logging.info(f"{num_questions} questions generated.")

    # Save to JSON
    if st.sidebar.button("Save Questions to JSON"):
        if st.session_state.get("original_questions"):
            filename = "questions.json"

            questions_to_save = {}

            for spec, questions in st.session_state.original_questions.items():
                questions_to_save[spec] = {
                    "questions": [
                        {
                            "id": q_id,
                            "question": q.get("question", ""),
                            "options": q.get("options", {}),
                            "correct_answer": q.get("correct_answer", ""),
                            "translations": q.get("translations", {})
                        }
                        for q_id, q in questions.items()
                    ]
                }

            save_to_json_in_english(filename, questions_to_save)
            st.sidebar.success(f"Questions saved as {filename}.")
        else:
            st.sidebar.error("No questions to save.")

    # Clear questions for demo
    if st.sidebar.button("Clear Questions"):
        st.session_state.original_questions = {}
        st.session_state.last_index = {}
        st.session_state.answer_feedback = {}
        st.session_state.explanation_result = {}
        st.session_state.prerequisite_result = {}
        st.session_state.similar_result = {}
        st.sidebar.success("Questions cleared.")
        st.rerun()

    # Display Questions and Check Answer
    if st.session_state.get("original_questions"):
        display_counter = 0

        for specialization, questions in st.session_state.original_questions.items():
            st.header(f"Topic: {specialization}")

            for i, (q_id, q) in enumerate(questions.items(), start=1):
                display_counter += 1
                safe_key = f"question_{display_counter}"

                st.markdown("---")
                st.subheader(f"Question {i}")

                left_col, right_col = st.columns([1.1, 1.8], gap="large")

                with left_col:
                    st.write(q["question"])

                    option_labels = list(q["options"].keys())

                    user_answer = st.radio(
                        "Options",
                        option_labels,
                        format_func=lambda x: f"{x}. {q['options'][x]}",
                        key=f"radio_{safe_key}"
                    )

                    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4, gap="small")

                    with col_btn1:
                        if st.button("Check", key=f"check_{safe_key}", use_container_width=True):
                            correct_answer = q["correct_answer"]

                            if isinstance(correct_answer, list):
                                correct_answer = correct_answer[0] if correct_answer else ""

                            correct_answer = str(correct_answer).strip().upper()

                            if correct_answer:
                                correct_answer = correct_answer[0]

                            if user_answer == correct_answer:
                                st.session_state.answer_feedback[safe_key] = {
                                    "type": "success",
                                    "message": "Correct!"
                                }
                            else:
                                st.session_state.answer_feedback[safe_key] = {
                                    "type": "error",
                                    "message": f"Incorrect. The correct answer is {correct_answer}: {q['options'].get(correct_answer, '')}"
                                }
                    with col_btn2:
                        if st.button("Explain", key=f"explain_{safe_key}", use_container_width=True):
                            with st.spinner(f"Explaining Question {i}..."):
                                if model:
                                    prompt_builder = PromptBuilder()
                                    prompt = prompt_builder.get_explain_answer_prompt(
                                        q["question"],
                                        q["options"],
                                        q["correct_answer"]
                                    )

                                    response = litellm.completion(
                                        model=model,
                                        messages=[
                                            {
                                                "role": "system",
                                                "content": "You are an expert assistant providing clear explanations for multiple-choice questions."
                                            },
                                            {
                                                "role": "user",
                                                "content": prompt
                                            }
                                        ],
                                        max_tokens=max_tokens_explanation
                                    )

                                    explanation = response.choices[0].message.content
                                    st.session_state.explanation_result[safe_key] = explanation
                                else:
                                    st.session_state.explanation_result[safe_key] = "Please select a valid model."
                    with col_btn3:
                        if st.button("Prereq", key=f"prereq_{safe_key}", use_container_width=True):
                            with st.spinner(f"Fetching prerequisite material for Question {i}..."):
                                if model:
                                    question_prerequisite = QuestionPrerequisite(model)
                                    prerequisite_material = question_prerequisite.question_prerequisites(
                                        q["question"],
                                        q["options"]
                                    )

                                    if isinstance(prerequisite_material, list):
                                        prerequisite_material = "\n\n".join(prerequisite_material)
                                        
                                    st.session_state.prerequisite_result[safe_key] = prerequisite_material
                                else:
                                    st.session_state.prerequisite_result[safe_key] = "Please select a valid model."
                    with col_btn4:
                        if st.button("Similar", key=f"similar_{safe_key}", use_container_width=True):
                            with st.spinner(f"Generating similar question for Question {i}..."):
                                if model:
                                    similar_question_generator = SimilarQuestionGenerator(model)
                                    similar_question = similar_question_generator.generate_similar_question(
                                        q["question"]
                                    )

                                    if isinstance(similar_question, list):
                                        similar_question = "\n\n".join(similar_question)

                                    st.session_state.similar_result[safe_key] = similar_question
                                else:
                                    st.session_state.similar_result[safe_key] = "Please select a valid model."

                with right_col:
                    st.markdown("#### Result Panel")

                    feedback = st.session_state.answer_feedback.get(safe_key)

                    if feedback:
                        if feedback["type"] == "success":
                            st.success(feedback["message"])
                        else:
                            st.error(feedback["message"])
                    else:
                        st.info("Select an option and click Check.")

                    explanation = st.session_state.explanation_result.get(safe_key)

                    if explanation:
                        with st.expander("Explanation", expanded=True):
                            st.write(explanation)

                    prerequisite = st.session_state.prerequisite_result.get(safe_key)

                    if prerequisite:
                        with st.expander("Prerequisite Knowledge", expanded=True):
                            st.write(prerequisite)
                    
                    similar = st.session_state.similar_result.get(safe_key)

                    if similar:
                        with st.expander("Similar Question", expanded=True):
                            st.write(similar)

if __name__ == "__main__":
    main()
