import streamlit as st
import requests
import json

def send_message(prompts):
    api_url = "https://api.anthropic.com/v1/complete"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": st.secrets["API_KEY"]
    }

    last_message = prompts[-1]['content']
    conversation = f"Human: {last_message}\n\nAssistant:"

    body = {
        "prompt": conversation,
        "model": "claude-2.0",
        "max_tokens_to_sample": 100000,
        "temperature": 0.6,
        "stop_sequences": ["\n\nHuman:"]
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(body))
        response.raise_for_status()
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

    result = response.json()
    return result['completion'].strip()

st.title("Chat with Claude")
st.write("Welcome to our chat app!")

if "prompts" not in st.session_state:
    st.session_state.prompts = []

if "new_message" not in st.session_state:
    st.session_state.new_message = False

for prompt in st.session_state.prompts:
    with st.chat_message(prompt['role']):
        st.write(prompt['content'])

if not st.session_state.new_message:
    user_message = st.chat_input("Say something")
    if user_message:
        st.session_state.new_message = True
        st.session_state.prompts.append({"role": "Human", "content": user_message})
        with st.spinner(text='Writing...'):
            response_from_claude = send_message(st.session_state.prompts)
            st.session_state.prompts.append({"role": "Assistant", "content": response_from_claude})
            st.experimental_rerun()

if st.button('Restart'):
    st.session_state.prompts = []
    st.session_state.new_message = False
    st.experimental_rerun()
