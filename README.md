# MCQ Generator using LLM

MCQ Generator is an AI-powered web application that uses Large Language Models (LLMs) to generate multiple-choice questions for Computer Science learning and instruction.

The project explores how LLMs can support Computer Science education by automating question generation, answer checking, answer explanation, prerequisite knowledge generation, and similar question creation.

## Project Topic

**Exploring How LLMs Can Automate Computer Science Instruction**

This project focuses on using LLMs as an assistant for instructors and students. Instead of manually creating quiz questions and explanations, users can input a Computer Science topic and allow the system to generate structured learning materials automatically.

## Features

### 1. MCQ Question Generation

Users can generate multiple-choice questions based on a selected Computer Science topic and difficulty level.

Example topics:

* Python Programming - Functions and Loops
* Basic SQL - SELECT and WHERE
* Object-Oriented Programming - Classes and Objects
* Computer Networks - DNS and DHCP
* Operating Systems - Process Scheduling
* Data Structures - Stack and Queue

### 2. Model Selection

The application supports model selection through LiteLLM.

Current model options include:

* Gemini 2.5 Flash-Lite
* Gemini 2.5 Flash
* OpenAI GPT-4o mini

Gemini 2.5 Flash-Lite is suitable for fast and cost-efficient question generation, while stronger models can be used when more detailed explanations are needed.

### 3. Difficulty Selection

Users can choose the difficulty level of generated questions:

* Easy
* Medium
* Hard

This allows the system to generate questions suitable for different learning levels.

### 4. Answer Checking

After questions are generated, users can select an answer and check whether it is correct.

The system provides immediate feedback by showing whether the selected answer is correct or incorrect.

### 5. Answer Explanation

Users can request an explanation for each question.

The explanation helps students understand why the correct answer is correct and why other options may be incorrect.

### 6. Prerequisite Knowledge Generation

The system can generate prerequisite knowledge for a selected question.

This feature provides background concepts and definitions that help students understand the question before answering it.

### 7. Similar Question Generation

Users can generate a similar question based on an existing question.

This helps students practice the same concept in a different form and supports reinforcement learning.

### 8. Save Questions to JSON

Generated questions can be saved into a JSON file.

The JSON file stores the generated questions in a structured format, including:

* Question ID
* Question text
* Options
* Correct answer
* Translations field for possible future extension

The JSON file is mainly designed for system reuse, future question bank development, and possible integration with databases or learning platforms.

## Tech Stack

* Python
* Streamlit
* LiteLLM
* Gemini API
* OpenAI API
* JSON

## Project Structure

```text
mcq_generator/
│
├── apps/
│   └── streamlit_apps/
│       └── main.py
│
├── src/
│   └── mcq_generator/
│       ├── mcq_generator.py
│       ├── prompt_builder.py
│       ├── question_generator.py
│       ├── question_prerequsite.py
│       └── similar_question_generator.py
│
├── tests/
│
├── requirements.txt
├── questions.json
└── README.md
```

## Main Components

### `main.py`

This is the main Streamlit application file.

It provides the web interface and connects user input with the backend modules. It allows users to generate questions, check answers, request explanations, generate prerequisite knowledge, generate similar questions, and save results to JSON.

### `mcq_generator.py`

This file contains the core MCQ generation logic.

It includes classes for generating questions, parsing LLM responses, validating input, saving questions, loading questions, and displaying questions.

### `prompt_builder.py`

This file builds prompts for different LLM tasks, such as:

* MCQ generation
* Answer explanation
* Prerequisite knowledge generation
* Similar question generation

Prompt engineering is an important part of this project because the quality of generated questions depends heavily on the prompt design.

### `question_prerequsite.py`

This file generates prerequisite knowledge for a selected question.

It helps students understand the background concepts needed to answer the question.

### `similar_question_generator.py`

This file generates similar questions based on an existing question.

It supports additional practice and concept reinforcement.

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/mcq-generator.git
cd mcq-generator
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## API Key Setup

To use Gemini models, set your Gemini API key:

```bash
$env:GEMINI_API_KEY="your_gemini_api_key"
```

To use OpenAI models, set your OpenAI API key:

```bash
$env:OPENAI_API_KEY="your_openai_api_key"
```

For the current demo, Gemini is recommended.

## Run the Application

Run the Streamlit app:

```bash
streamlit run apps/streamlit_apps/main.py
```

After running the command, the app will open in the browser.

## How to Use

1. Select a model.
2. Enter or select a Computer Science topic.
3. Choose the difficulty level.
4. Choose the number of questions.
5. Click **Generate Questions**.
6. Select an answer and click **Check**.
7. Click **Explain** to get an explanation.
8. Click **Prereq** to get prerequisite knowledge.
9. Click **Similar** to generate a similar practice question.
10. Click **Save Questions to JSON** to save the generated questions.

## Example Demo Topic

Recommended topic for demo:

```text
Python Programming - Functions and Loops
```

Recommended settings:

```text
Model: gemini/gemini-2.5-flash-lite
Difficulty: Easy
Number of questions: 3
```

This topic is simple, easy to verify, and suitable for demonstrating the main features of the system.

## Example JSON Output

```json
{
  "Python Programming - Functions and Loops": {
    "questions": [
      {
        "id": "Python Programming - Functions and Loops_1",
        "question": "Which keyword is used to define a function in Python?",
        "options": {
          "A": "func",
          "B": "define",
          "C": "def",
          "D": "function"
        },
        "correct_answer": "C",
        "translations": {}
      }
    ]
  }
}
```

## Purpose of JSON Storage

The JSON file is not mainly designed for human reading. It stores generated questions in a structured format so that the system can reuse them later or integrate them into a future database, question bank, or learning platform.

## Educational Value

This project demonstrates how LLMs can support Computer Science instruction by automating repetitive teaching tasks.

The system can help with:

* Creating practice questions
* Providing immediate feedback
* Explaining correct answers
* Preparing prerequisite knowledge
* Creating similar practice questions
* Saving generated questions for reuse

The project does not aim to replace instructors. Instead, it acts as an assistant that can reduce preparation time and support students during self-study.

## Limitations

Although LLMs can generate useful educational content, the output may still contain errors or unclear explanations.

Main limitations include:

* Generated questions may sometimes be incorrect.
* Correct answers may need human verification.
* Explanations may be too long or too general.
* Some technical topics may require instructor review.
* The current version uses JSON storage instead of a full database.

Therefore, human review is still necessary before using generated questions in formal assessments.

## Future Work

Possible future improvements include:

* Integrating a database for question storage
* Supporting user accounts
* Adding question editing features
* Adding more question types
* Integrating with learning management systems
* Adding automatic quality checking for generated questions
* Supporting analytics for student performance

## Conclusion

The MCQ Generator shows how LLMs can be used to automate parts of Computer Science instruction. By generating questions, explanations, prerequisite knowledge, and similar practice questions, the system provides a practical example of how AI can support both instructors and students in the learning process.
