import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="NOVA AI", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .center-title {
            font-size: 100px;
            font-weight: bold;
            text-align: center;
            color: #31333F;
        }
    </style>
    <h1 class="center-title">✨ NOVA AI ✨</h1>
""", unsafe_allow_html=True)

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("Please add your Gemini API key to the Streamlit secrets manager. Create a file .streamlit/secrets.toml with the line: GEMINI_API_KEY = 'YOUR_KEY_HERE'")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while configuring the Gemini API: {e}")
    st.stop()

model = genai.GenerativeModel('gemini-pro')

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]

st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }
        .chat-container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            color: #4CAF50;
            margin-bottom: 20px;
        }
        .message {
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
        }
        .user {
            align-items: flex-end;
        }
        .assistant {
            align-items: flex-start;
        }
        .message-content {
            padding: 10px;
            border-radius: 20px;
            max-width: 70%;
        }
        .user .message-content {
            background-color: #DCF8C6;
            color: #000000;
            border-bottom-right-radius: 5px;
        }
        .assistant .message-content {
            background-color: #E0F7FA;
            color: #000000;
            border-bottom-left-radius: 5px;
        }
        .input-container {
            margin-top: 20px;
            display: flex;
        }
        .text-input {
            flex: 1;
            padding: 12px 15px;
            border: 1px solid #ccc;
            border-radius: 25px;
            margin-right: 10px;
            font-size: 16px;
            border-color: #4CAF50;
            background-color: #F0FFF0;
        }
        .text-input:focus {
            outline: none;
            border-color: #388E3C;
            box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
        }
        .send-button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .send-button:hover {
            background-color: #388E3C;
        }
        @media (max-width: 600px) {
            .chat-container {
                padding: 10px;
            }
            .message-content {
                max-width: 90%;
            }
            .text-input {
                font-size: 14px;
                padding: 10px;
            }
            .send-button {
                font-size: 14px;
                padding: 10px 18px;
            }
        }
    </style>
""", unsafe_allow_html=True)

chat_container = st.container()
with chat_container:
    st.markdown('<h1 class="header">Gemini Chatbot</h1>', unsafe_allow_html=True)
    for message in st.session_state.messages:
        message_alignment = "user" if message["role"] == "user" else "assistant"
        st.markdown(
            f'<div class="message {message_alignment}">'
            f'<div class="message-content">'
            f'{message["content"]}'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    input_container = st.container()
    with input_container:
        col1, col2 = st.columns([0.75, 0.25])
        prompt = col1.text_input("Enter your message...", key="prompt", label_visibility="collapsed", placeholder="Type your message...")
        send_button = col2.button("Send", key="send_button")

    if send_button and prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"An error occurred: {e}")
        st.session_state["prompt"] = ""
        st.rerun()
