import streamlit as st
import requests
import json

def send_message(prompts):
    api_url = "https://api.anthropic.com/v1/complete"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": st.secrets["API_KEY"]
    }

    # Prepare the prompts for Claude
    conversation = "\n\n".join([f'{item["role"]}: {item["content"]}' for item in prompts]) + "\n\nAssistant:"

    body = {
        "prompt": conversation,
        "model": "claude-2.0",
        "stop_sequences": ["\n\nHuman:"]
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(body))
    response.raise_for_status()

    return response.json()

st.title("Chat with Claude")
st.write("Welcome to our chat app!")

if "prompts" not in st.session_state:
    st.session_state.prompts = []

# Display the entire conversation
for prompt in st.session_state.prompts:
    with st.chat_message(prompt['role']):
        st.write(prompt['content'])

# Capture and display user's message
user_message = st.chat_input("Say something")
if user_message:
    st.session_state.prompts.append({"role": "Human", "content": user_message})
    try:
        result = send_message(st.session_state.prompts)

        # Append Claude's response to the prompts
        st.session_state.prompts.append({
            "role": "Assistant",
            "content": result['completion']
        })
        
        # Rerun the script to update the chat
        st.experimental_rerun()

    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        st.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        st.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        st.error(f"Something went wrong: {err}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

if st.button('Restart'):
    st.session_state.prompts = []
    st.experimental_rerun()
