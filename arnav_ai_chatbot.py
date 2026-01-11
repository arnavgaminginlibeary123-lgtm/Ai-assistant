import streamlit as st
import os
import openai
import requests
import json
import re
from datetime import datetime

# Page config
st.set_page_config(page_title="Arnav AI Chatbot", page_icon="🤖", layout="wide")

# API Keys from Streamlit secrets
openai.api_key = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

class InternetAIChatbot:
    def __init__(self):
        self.conversation_history = []
        self.max_history = 10

    def google_search(self, query):
        try:
            headers = {
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            }
            data = {"q": query, "num": 3}
            response = requests.post("https://google.serper.dev/search", headers=headers, json=data)
            results = response.json()
            search_results = []
            for result in results.get("organic", []):
                search_results.append(f"• **{result.get('title', '')}**
{result.get('snippet', '')}")
            return "
".join(search_results) if search_results else "No results found."
        except Exception as e:
            return f"Search error: {str(e)}"

    def get_weather(self, city):
        try:
            url = f"http://api.weatherapi.com/v1/current.json"
            params = {"key": WEATHER_API_KEY, "q": city}
            response = requests.get(url, params=params)
            data = response.json()
            current = data["current"]
            location = data["location"]
            return f"🌤️ **{location['name']}, {location['country']}**
{current['temp_c']}°C, {current['condition']['text']}
Feels like: {current['feelslike_c']}°C"
        except Exception as e:
            return f"Weather error for {city}: {str(e)}"

    def detect_intent(self, user_input):
        user_input_lower = user_input.lower()
        if any(word in user_input_lower for word in ["weather", "temperature", "rain"]):
            city_match = re.search(r'(?:ins+)?([a-zA-Zs]+?)(?:?|!|$)', user_input_lower)
            return "weather", city_match.group(1).strip() if city_match else "Delhi"
        elif any(word in user_input_lower for word in ["search", "google", "find", "what is"]):
            query = re.sub(r'(?:search|google|find).*?(fors*)?', '', user_input, flags=re.IGNORECASE).strip()
            return "search", query
        return "chat", ""

    def get_openai_response(self, user_input, context=""):
        try:
            messages = [
                {
                    "role": "system",
                    "content": f"You are ArnavBot, made by Arnav Srivastava. Helpful AI with internet access. Context: {context}"
                },
                {"role": "user", "content": user_input}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=400,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"AI error: {str(e)}"

    def process_message(self, user_input):
        intent, param = self.detect_intent(user_input)
        context = ""

        if intent == "weather":
            context = self.get_weather(param)
            response = self.get_openai_response(user_input, f"Weather: {context}")
        elif intent == "search":
            context = self.google_search(param)
            response = self.get_openai_response(user_input, f"Search: {context}")
        else:
            response = self.get_openai_response(user_input)

        self.conversation_history.append({"user": user_input, "bot": response})
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
        return response

# ========== STREAMLIT UI ==========
st.title("🤖 Arnav AI Chatbot")
st.markdown("**Made by Arnav Srivastava** | 🌐 Internet Search | 🌤️ Weather | 🧠 GPT")

# Sidebar
with st.sidebar:
    st.header("🔑 API Status")
    st.info(f"**OpenAI**: {'✅ Ready' if openai.api_key else '❌ Missing'}")
    st.info("**Google**: Serper API")
    st.info("**Weather**: WeatherAPI")
    st.markdown("---")
    st.markdown("[⭐ Star on GitHub](https://github.com/yourusername/arnav-ai-chatbot)")

# Initialize session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = InternetAIChatbot()
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("💬 Ask anything... (weather Delhi, search Python, etc.)"):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot response
    with st.chat_message("assistant"):
        with st.spinner("🤖 ArnavBot is thinking..."):
            response = st.session_state.chatbot.process_message(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Footer
st.markdown("---")
st.markdown("*Deployed on Streamlit Cloud | Made by Arnav Srivastava 🚀*")
