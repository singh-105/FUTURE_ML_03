# 🤖 AI Customer Support Chatbot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://futureml03-bw9xqqzcpm9ezvcyd6vshx.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Dialogflow](https://img.shields.io/badge/Google-Dialogflow_ES-orange)
![Status](https://img.shields.io/badge/Status-Deployed-success)

### 🚀 **Live Demo:** [Click Here to Chat with the Bot](https://futureml03-bw9xqqzcpm9ezvcyd6vshx.streamlit.app/)

---

## 📸 Project Screenshot
![App Screenshot](https://via.placeholder.com/800x400?text=Upload+Your+App+Screenshot+Here)

---

## 📖 Overview
This project is an **AI-powered Customer Support Assistant** designed to automate interactions for an e-commerce platform. It leverages **Google Dialogflow** for natural language understanding (NLU) and **Streamlit** for a responsive web interface.

Unlike simple rule-based bots, this assistant uses a **Hybrid Approach**:
1.  **Intents:** For structured workflows (e.g., tracking orders with dynamic ID inputs).
2.  **Knowledge Base:** For unstructured FAQs (e.g., shipping policies, refunds) derived from a cleaned dataset.

## ✨ Key Features
* **Order Tracking:** Intelligently asks for Order ID and retrieves status (simulated).
* **Smart FAQs:** Instantly answers questions about refunds, shipping, and technical issues using a Knowledge Base.
* **Context Awareness:** Maintains session state to handle follow-up questions naturally (e.g., remembering the user is asking about a specific order).
* **Secure Cloud Deployment:** Hosted on Streamlit Cloud using **Secrets Management** to protect Google Cloud credentials.

---

## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/) (Python)
* **AI Engine:** [Google Dialogflow ES](https://cloud.google.com/dialogflow)
* **Language:** Python 3.10+
* **Deployment:** Streamlit Cloud + GitHub
* **Version Control:** Git

---

## ⚙️ Installation & Local Setup

If you want to run this project on your own machine:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/singh-105/FUTURE_ML_03.git](https://github.com/singh-105/FUTURE_ML_03.git)
    cd FUTURE_ML_03
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Setup Google Credentials:**
    * Download your `credentials.json` from Google Cloud Console.
    * Place it in the root folder.
    * *Note: This file is git-ignored for security.*

5.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

---

## 🧠 How It Works (Architecture)

1.  **User Input:** The user types a query in the Streamlit interface.
2.  **Dialogflow API:** The app sends the text to Google Dialogflow.
3.  **Intent Matching:**
    * If it matches an **Intent** (e.g., "Where is my order?"), the bot triggers the specific workflow.
    * If it matches a **Knowledge Base FAQ**, the bot pulls the answer from the CSV data.
4.  **Response:** The text response is sent back to Streamlit and displayed in the chat window.

---

## 🛡️ Security
This project follows industry best practices for security:
* **No Hardcoded Keys:** API keys are not stored in the code.
* **Streamlit Secrets:** In production, credentials are injected via Streamlit's encrypted Secrets Manager.
* **.gitignore:** Sensitive files (`credentials.json`, `venv`) are excluded from the repository.

---

## 👨‍💻 Author
**Harsh Singh**
* **GitHub:** [singh-105](https://github.com/singh-105)
* **Project Link:** [Streamlit App](https://futureml03-bw9xqqzcpm9ezvcyd6vshx.streamlit.app/)

---
*Created as part of an AI/ML Internship Project.*