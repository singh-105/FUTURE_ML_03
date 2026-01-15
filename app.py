import streamlit as st
from google.cloud import dialogflow
from google.oauth2 import service_account
import os
import json
import uuid
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Support Bot", page_icon="🤖", layout="wide")

# --- AUTHENTICATION (CLOUD + LOCAL SUPPORT) ---
if "gcp_service_account" in st.secrets:
    # 1. Try loading from Streamlit Cloud Secrets
    service_account_info = st.secrets["gcp_service_account"]
    PROJECT_ID = service_account_info["project_id"]
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    session_client = dialogflow.SessionsClient(credentials=credentials)

elif os.path.exists("credentials.json"):
    # 2. Fallback to Local File (for your laptop)
    with open("credentials.json", 'r') as f:
        data = json.load(f)
        PROJECT_ID = data['project_id']
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
    session_client = dialogflow.SessionsClient()

else:
    # 3. If both fail
    st.error("❌ Authentication Error: Could not find 'credentials.json' locally, and 'st.secrets' are missing on the cloud.")
    st.stop()

SESSION_ID = "user_session_" + str(uuid.uuid4())

# --- DIALOGFLOW FUNCTION ---
def get_dialogflow_response(text):
    session = session_client.session_path(PROJECT_ID, SESSION_ID)
    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text

# --- UI LAYOUT ---
st.sidebar.title("📜 History")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
st.title("🤖 Customer Support Assistant")
st.markdown("Ask about **Order Status**, **Refunds**, or **Tech Issues**.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    if message["role"] == "user":
        timestamp = datetime.datetime.now().strftime("%H:%M")
        st.sidebar.text(f"[{timestamp}] {message['content']}")

# Input
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