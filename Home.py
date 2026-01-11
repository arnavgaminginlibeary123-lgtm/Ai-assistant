import streamlit as st
import os
from arnav_ai_chatbot import InternetAIChatbot
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Arnav AI Chatbot", page_icon="🤖")

if "chatbot" not in st.session_state:
    st.session_state.chatbot = InternetAIChatbot()

st.title("🤖 Arnav AI Chatbot")
st.markdown("**Made by Arnav Srivastava**")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chatbot.process_message(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
