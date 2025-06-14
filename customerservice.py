import streamlit as st
import json
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# JSON log file
LOG_FILE = "customer_service_log.json"

# App title
st.title("Customer Service & Feedback Bot")

# Initialize chat history in session
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": (
            "You are a helpful and polite customer service assistant. "
            "You assist users with inquiries, product issues, or take feedback. "
            "Always stay on topic and decline to answer unrelated questions."
        )}
    ]

# Save interaction to JSON file
def log_to_json(user_input, assistant_reply, file_path=LOG_FILE):
    entry = {
        "user": user_input,
        "assistant": assistant_reply
    }

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Display chat history
for msg in st.session_state.messages[1:]:  # skip system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box
user_input = st.chat_input("Let us know your issue or feedback...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get assistant response
    def get_response():
        chat_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        return chat_response.choices[0].message.content

    response = get_response()

    # Save interaction
    log_to_json(user_input, response)

    # Show assistant reply
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
