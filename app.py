import streamlit as st
import os
from connect import main_chatbot

# ---- Constants ----
EXCEL_PATH = "latest_file.xlsx"

# ---- Page Config ----
st.set_page_config(page_title="KRISPR Digital Business Analyst", layout="centered")

# ---- CSS Styling ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, .stApp {
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
    }

    .main-title {
        text-align: center;
        font-size: 2em;
        font-weight: 600;
        color: #222;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    .chat-box {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 0 1rem 6rem;
        max-width: 800px;
        margin: 0 auto;
    }

    .message {
        max-width: 85%;
        padding: 0.9rem 1.2rem;
        border-radius: 12px;
        font-size: 1rem;
        line-height: 1.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.04);
    }

    .user {
        align-self: flex-end;
        background-color: #e6f0ff;
        color: #000;
        border-top-right-radius: 0;
    }

    .bot {
        align-self: flex-start;
        background-color: #f2f2f2;
        color: #000;
        border-top-left-radius: 0;
    }

    .input-area {
        position: fixed;
        bottom: 1.5rem;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 800px;
        background: #fff;
        display: flex;
        gap: 0.5rem;
        padding: 0.75rem 1rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.03);
        border-radius: 12px;
        z-index: 10;
    }

    input[type="text"] {
        flex-grow: 1;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border: 1px solid #ccc;
        font-size: 1rem;
    }

    button {
        background-color: #000;
        color: #fff;
        padding: 0.75rem 1.2rem;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        cursor: pointer;
        font-size: 1rem;
    }

    button:hover {
        background-color: #333;
    }

    footer, header, .stProgress {
        display: none !important;
    }

    .block-container {
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---- Title ----
st.markdown('<div class="main-title">KRISPR Digital Business Analyst</div>', unsafe_allow_html=True)

# ---- Check Excel file ----
if not os.path.exists(EXCEL_PATH):
    st.warning("⚠️ No Excel file found. Please ask the admin to upload it.")
    st.stop()

# ---- Init Chat ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- Chat Display ----
st.markdown('<div class="chat-box">', unsafe_allow_html=True)
for role, msg in st.session_state.chat_history:
    role_class = "user" if role == "user" else "bot"
    st.markdown(f'<div class="message {role_class}">{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---- Input Area ----
with st.form("chat_form", clear_on_submit=True):
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="Ask your business question...", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Handle Chat ----
if submitted and user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Analyzing..."):
        try:
            answer = main_chatbot(user_input, EXCEL_PATH)
            st.session_state.chat_history.append(("bot", answer))
        except Exception as e:
            st.session_state.chat_history.append(("bot", f"⚠️ Error: {e}"))
    st.rerun()
