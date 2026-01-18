import streamlit as st
from google.cloud import dialogflow
from google.oauth2 import service_account
import os
import json
import uuid
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Support Bot", page_icon="🤖", layout="wide")

# --- AUTHENTICATION ---
if "gcp_service_account" in st.secrets:
    service_account_info = st.secrets["gcp_service_account"]
    PROJECT_ID = service_account_info["project_id"]
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    session_client = dialogflow.SessionsClient(credentials=credentials)
elif os.path.exists("credentials.json"):
    with open("credentials.json", 'r') as f:
        data = json.load(f)
        PROJECT_ID = data['project_id']
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
    session_client = dialogflow.SessionsClient()
else:
    st.error("❌ Authentication Error: Keys missing!")
    st.stop()

# --- FIX: PERSIST SESSION ID ---
if "session_id" not in st.session_state:
    st.session_state.session_id = "user_session_" + str(uuid.uuid4())

SESSION_ID = st.session_state.session_id

# --- DIALOGFLOW FUNCTION ---
def get_dialogflow_response(text):
    session = session_client.session_path(PROJECT_ID, SESSION_ID)
    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)
    # We removed the broken "knowledge_base" code here to stop the crash
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text

# --- UI LAYOUT ---
st.sidebar.title("📜 History")
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Customer Support Assistant")
st.markdown("Ask about **Order Status**, **Refunds**, or **Tech Issues**.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    if message["role"] == "user":
        timestamp = datetime.datetime.now().strftime("%H:%M")
        st.sidebar.text(f"[{timestamp}] {message['content']}")

if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("..."):
        bot_reply = get_dialogflow_response(prompt)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.rerun()