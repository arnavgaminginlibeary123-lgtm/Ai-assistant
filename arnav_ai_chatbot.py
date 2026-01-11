"""
Arnav AI Chatbot - Final Production Version
Made by Arnav Srivastava
Fix: Strict OpenAI v1.0+ initialization to prevent TypeError
"""

import os
import requests
import json
import re
from openai import OpenAI

# ========== INITIALIZATION ==========
# We fetch the key directly from the environment
_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize client outside the class to ensure it only happens once
# This prevents the "__init__" error seen in your screenshot
client = OpenAI(api_key=_API_KEY)

class InternetAIChatbot:
    def __init__(self):
        self.conversation_history = []
        self.max_history = 10
        self.serper_key = os.getenv("SERPER_API_KEY")
        self.weather_key = os.getenv("WEATHER_API_KEY")

    def google_search(self, query: str) -> str:
        if not self.serper_key:
            return "Search unavailable: Missing API Key."
        try:
            headers = {"X-API-KEY": self.serper_key, "Content-Type": "application/json"}
            payload = {"q": query, "num": 3}
            response = requests.post(
                "https://google.serper.dev/search", 
                headers=headers, 
                json=payload, 
                timeout=10
            )
            results = response.json()
            items = [f"{r.get('title')}: {r.get('snippet')}" for r in results.get("organic", [])]
            return "\n".join(items) if items else "No results found."
        except Exception as e:
            return f"Search error: {str(e)}"

    def get_weather(self, city: str) -> str:
        if not self.weather_key:
            return "Weather unavailable: Missing API Key."
        try:
            url = f"http://api.weatherapi.com/v1/current.json?key={self.weather_key}&q={city}"
            response = requests.get(url, timeout=10)
            data = response.json()
            if "error" in data: return f"City {city} not found."
            return f"Weather in {data['location']['name']}: {data['current']['temp_c']}°C, {data['current']['condition']['text']}."
        except Exception:
            return "Weather service error."

    def detect_intent(self, text: str) -> tuple:
        t = text.lower()
        # Improved regex for city extraction
        w_match = re.search(r'(?:weather|temp|temperature)\s+(?:in|at|for)\s+([a-zA-Z\s]+)', t)
        if w_match:
            return "weather", w_match.group(1).strip()
        if any(x in t for x in ["search", "google", "find"]):
            query = re.sub(r'(search|google|find)', '', t).strip()
            return "search", query if query else t
        return "chat", ""

    def get_openai_response(self, user_input: str, context: str = "") -> str:
        try:
            messages = [
                {"role": "system", "content": f"You are ArnavBot by Arnav Srivastava. Real-time data: {context}"}
            ]
            # Include history for context
            for h in self.conversation_history[-3:]:
                messages.append({"role": "user", "content": h["user"]})
                messages.append({"role": "assistant", "content": h["bot"]})
            
            messages.append({"role": "user", "content": user_input})

            # FIXED CALL: No extra arguments that cause TypeErrors
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Error: {str(e)}"

    def process_message(self, user_input: str) -> str:
        intent, param = self.detect_intent(user_input)
        context = ""
        if intent == "weather":
            context = self.get_weather(param)
        elif intent == "search":
            context = self.google_search(param)
        
        bot_res = self.get_openai_response(user_input, context)
        self.conversation_history.append({"user": user_input, "bot": bot_res})
        return bot_res
