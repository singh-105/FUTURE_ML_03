import streamlit as st
from google.cloud import dialogflow
import os
import json
import uuid
import datetime

# --- CONFIGURATION ---
CREDENTIALS_FILE = "credentials.json"
SESSION_ID = "user_session_123"

# --- SETUP DIALOGFLOW ---
if os.path.exists(CREDENTIALS_FILE):
    with open(CREDENTIALS_FILE, 'r') as f:
        data = json.load(f)
        PROJECT_ID = data['project_id']
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_FILE
else:
    st.error("❌ Error: 'credentials.json' file not found!")
    st.stop()

def get_dialogflow_response(text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, SESSION_ID)
    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text

# --- PAGE SETUP ---
st.set_page_config(page_title="Support Bot", page_icon="🤖", layout="wide")

# --- SIDEBAR (HISTORY) ---
st.sidebar.title("📜 Session History")
st.sidebar.write("Here is a log of your questions:")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MAIN CHAT INTERFACE ---
st.title("🤖 Customer Support Assistant")
st.markdown("Ask about **Order Status** or **Technical Issues** (Heating, Battery, etc.)")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # ADD TO SIDEBAR LOG (Only User Questions)
    if message["role"] == "user":
        timestamp = datetime.datetime.now().strftime("%H:%M")
        st.sidebar.text(f"[{timestamp}] {message['content']}")

# User Input
if prompt := st.chat_input("Type your message here..."):
    # 1. Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get Bot Response
    with st.spinner("Thinking..."):
        bot_reply = get_dialogflow_response(prompt)

    # 3. Show Bot Message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    
    # 4. Force Sidebar Update
    st.rerun()