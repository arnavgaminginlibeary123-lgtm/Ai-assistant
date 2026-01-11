"""
Arnav AI Chatbot - Complete Internet AI Assistant
Made by Arnav Srivastava
Fixed: No spaces, no import errors, production ready
"""

import os
import openai
import requests
import json
import re
from datetime import datetime
from typing import List, Dict

# ========== CONFIGURATION ==========
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "your-serper-key")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "your-weather-key")

openai.api_key = OPENAI_API_KEY

class InternetAIChatbot:
    def __init__(self):
        self.conversation_history = []
        self.max_history = 10

    def google_search(self, query: str) -> str:
        if not SERPER_API_KEY or SERPER_API_KEY == "your-serper-key":
            return "❌ Google Search: Add SERPER_API_KEY"
        try:
            headers = {
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            }
            data = {"q": query, "num": 3}
            response = requests.post(
                "https://google.serper.dev/search",
                headers=headers,
                json=data,
                timeout=10
            )
            results = response.json()
            search_results = []
            for result in results.get("organic", [])[:3]:
                title = result.get('title', 'No title')
                snippet = result.get('snippet', '')
                search_results.append("f"**{title}**
{snippet}")
            return "

".join(search_results) if search_results else "No results found"
        except Exception as e:
            return f"Search error: {str(e)[:50]}"

    def get_weather(self, city: str = "Delhi") -> str:
        if not WEATHER_API_KEY or WEATHER_API_KEY == "your-weather-key":
            return "❌ Weather: Add WEATHER_API_KEY"
        try:
            url = "http://api.weatherapi.com/v1/current.json"
            params = {"key": WEATHER_API_KEY, "q": city}
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            location = data["location"]
            current = data["current"]
            return f"""🌤️ **{location['name']}, {location['country']}**
🌡️ {current['temp_c']}°C | {current['condition']['text']}
😊 Feels like: {current['feelslike_c']}°C"""
        except Exception as e:
            return f"Weather unavailable for {city}"

    def detect_intent(self, user_input: str) -> tuple:
        text = user_input.lower()
        if any(word in text for word in ["weather", "temperature", "rain", "temp"]):
            city_match = re.search(r'ins+([a-zA-Zs]+?)(?:?|!|$)', text)
            city = city_match.group(1).strip() if city_match else "Delhi"
            return "weather", city
        elif any(word in text for word in ["search", "google", "find", "what is"]):
            query = re.sub(r'(?:search|google|find).*?(fors*)?', '', text, flags=re.IGNORECASE).strip()
            query = query if query else text
            return "search", query
        return "chat", ""

    def get_openai_response(self, user_input: str, context: str = "") -> str:
        if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-key":
            return "❌ OpenAI: Add OPENAI_API_KEY to .env or secrets.toml"
        try:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are ArnavBot, made by Arnav Srivastava. "
                        "You are a helpful AI assistant with internet access. "
                        f"Weather/Search context: {context}"
                    )
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
            return f"🤖 AI Error: {str(e)[:100]}"

    def process_message(self, user_input: str) -> str:
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

    def chat(self):
        print("🤖 Arnav AI Chatbot - Made by Arnav Srivastava")
        print("=" * 60)
        print("Commands: 'weather Delhi', 'search Python', 'quit'")
        print("API Status:")
        print(f"  OpenAI: {'✅' if OPENAI_API_KEY != 'your-openai-key' else '❌'}")
        print(f"  Google: {'✅' if SERPER_API_KEY != 'your-serper-key' else '❌'}")
        print(f"  Weather: {'✅' if WEATHER_API_KEY != 'your-weather-key' else '❌'}")
        print("=" * 60)

        while True:
            user_input = input("
You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 ArnavBot: Goodbye! Made by Arnav Srivastava 🚀")
                break
            if not user_input:
                continue

            print("🤖 ArnavBot: ", end="", flush=True)
            response = self.process_message(user_input)
            print(response)

def save_conversation(history: List[Dict]):
    try:
        with open("chat_history.json", "w") as f:
            json.dump(history, f, indent=2)
    except:
        pass

def load_conversation() -> List[Dict]:
    try:
        with open("chat_history.json", "r") as f:
            return json.load(f)
    except:
        return []

# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    chatbot = InternetAIChatbot()
    print("🚀 Starting Arnav AI Chatbot!")
    print("📱 Features: GPT + Google Search + Weather API")
    print("👨‍💻 Made by Arnav Srivastava")
    chatbot.chat()
