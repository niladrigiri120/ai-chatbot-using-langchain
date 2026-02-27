# ---------- Importing Important Libraries ----------
import os
import time
import streamlit as st
from langchain_chatbot import model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# ---------- Page Title ----------
st.markdown(
    "<h1 style='text-align: center; color: #223854;'>Chatterly 🗣️</h1>",
    unsafe_allow_html=True
)

# ---------- Initialize Session State ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful AI assistant.")]
if "show_prompts" not in st.session_state:
    st.session_state.show_prompts = True

if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = None

# ---------- Display All Chat History----------
for msg in st.session_state.chat_history[1:]:  #Skip System Messege
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# ---------- Default Prompts Section ----------

if st.session_state.show_prompts:
    st.markdown("### 💡 Try one of these prompts:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🪶 Write a haiku about AI", key=1):
            st.session_state.prompt_input = "Write a haiku about AI"
        if st.button("🎯 Help me set 3 personal goals", key= 2):
            st.session_state.prompt_input = "Help me set 3 personal goals"
        if st.button("🧩 Give me 3 brain-teasing logic puzzles", key=3):
            st.session_state.prompt_input = "Give me 3 brain-teasing logic puzzles"
        if st.button("👔 Practice a job interview with me", key=4):
            st.session_state.prompt_input = "Practice a job interview with me"
        
    with col2:
        if st.button("✨ Give me a motivational quote", key=5):
            st.session_state.prompt_input = "Give me a motivational quote"
        if st.button("📘 Summarize the book Ikigai", key=6):
            st.session_state.prompt_input = "Summarize the book Ikigai"
        if st.button("🎁 Recommend some unique gift ideas", key=7):
            st.session_state.prompt_input = "Recommend some unique gift ideas"
        if st.button("✉️ Draft a polite follow-up email", key=8):
            st.session_state.prompt_input = "Draft a polite follow-up email"

# ---------- User input box ----------
text_input = st.chat_input("Type your message...")
user_input = st.session_state.get("prompt_input") or text_input

if user_input:
    st.session_state.show_prompts = False

    # Add user message
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Make a copy
    model_input = st.session_state.chat_history.copy()

    # Get model response

    with st.chat_message("assistant"):
        with st.spinner("Chatterly is thinking..."):
            messege_placeholder = st.empty()
            ai_response = ""

            for token in model.stream(model_input):
                ai_response += token.content
                messege_placeholder.markdown(ai_response)
                time.sleep(0.04)

    # Add AI message
    st.session_state.chat_history.append(AIMessage(content=ai_response))
    
    st.session_state.prompt_input = None

# ---------- Clear Chat ----------
cola, colb, colc, cold = st.columns(4)
with cold:
    if len(st.session_state.chat_history) >1:   #Show only after user_input
        if st.button("🧹Clear Chat"):
            st.session_state.chat_history = [
                SystemMessage(content="You are a helpful AI assistant.")
                ]
            st.session_state.show_prompts = True
            st.session_state.prompt_input = None

            st.rerun()
